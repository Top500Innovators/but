# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from notification import models as notification
from models import Invitation, Profile, Keyword, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages

def check_profile(code):
    try:
        return Profile.objects.get(key=code)
    except Profile.DoesNotExist:
        return None

def check_invitation(code):
    try:
        i = Invitation.objects.get(key=code)
        return True
    except:
        return False

def generate_key():
    import random
    return str(random.random())[2:]

def index(request):    
    from forms import ResetKeyForm
    if request.POST:
        form=ResetKeyForm(request.POST)
        if form.is_valid(): 
            try:
                p = Profile.objects.get(email=form.cleaned_data['email'])
            except Profile.DoesNotExist:
                messages.error(request, 'There is no user with this email addres, try again.')
                return render_to_response('researchers/index.html', {'form':form }, context_instance=RequestContext(request))
            p.key = generate_key()
            p.save()
            url = reverse('homepage', args=[p.key])
            u,created=User.objects.get_or_create(username=p.email[:30])
            notification.send([u], "remind", {'homepage': url})
            messages.info(request, 'Check your email account (%s), we have sent you an email.')
            return render_to_response('researchers/index.html', { 'form':ResetKeyForm() }, context_instance=RequestContext(request))
    else:
        form=ResetKeyForm()
    return render_to_response('researchers/index.html', { 'form':form }, context_instance=RequestContext(request))

def homepage(request, code):
    p = check_profile(code)
    if not p:
        messages.error(request, 'Your personal URL is incorrect, please reset your account or provide proper url')
        return HttpResponseRedirect(reverse(index)) 
    
    return render_to_response('researchers/dashboard.html', {'profile':p, 'key':code}, context_instance=RequestContext(request))

def __to_keywords(string):
    tags=string.split(',')
    keywords=[]
    for t in tags:
        k, created=Keyword.objects.get_or_create(value=t.strip())
        keywords.append(k)
    return keywords

def search(request, code):
    profile = check_profile(code)
    if not profile:
        messages.error(request, 'Your personal URL is incorrect, please reset your account or provide proper url')
        return redirect('index') 

    results={}
    from forms import SearchForm
    if request.method == 'POST':
        form = SearchForm(request.POST) 
        if form.is_valid(): 
            keywords = __to_keywords(form.cleaned_data['search'])
            for k in keywords:
                profiles = Profile.objects.filter(keywords=k)
                for p in profiles:
                    count = results.get(p, 0)
                    results[p]=count+1
            if len(results)==0:
                messages.error(request, "Sorry, we couldn't find match for you. Try later.")

    else:
        form=SearchForm()
    
    return render_to_response('researchers/search.html', {'profile':profile, 
                                                            'key':code, 
                                                            'form':form, 
                                                            'results':results,
                                                            'sorted':sorted(results.items(), key=lambda x: -x[1])}, 
                                            context_instance=RequestContext(request))


def test_search(request, code):
    invitation = check_invitation(code)
    if not invitation:
        messages.error(request, 'Your personal URL is incorrect, please reset your account or provide proper url')
        return redirect('index') 
    
    results={}
    from forms import SearchForm
    if request.method == 'POST':
        form = SearchForm(request.POST) 
        if form.is_valid(): 
            keywords = __to_keywords(form.cleaned_data['search'])
            for k in keywords:
                profiles = Profile.objects.filter(keywords=k)
                for p in profiles:
                    count = results.get(p, 0)
                    results[p]=count+1
            if len(results)==0:
                messages.error(request, "Sorry, we couldn't find match for you. Try later.")
    
    else:
        form=SearchForm()
    
    return render_to_response('researchers/test_search.html', {'key':code, 
                                                                'form':form, 
                                                                'results':results,
                                                                'sorted':sorted(results.items(), key=lambda x: -x[1])},  context_instance=RequestContext(request))






def invite(request, code):
    profile = check_profile(code)
    if not profile:
        messages.error(request, 'Your personal URL is incorrect, please reset your account or provide proper url')
        return redirect('index') 
    
    from forms import InvitationForm
    if request.method == 'POST':
        form = InvitationForm(request.POST) 
        if form.is_valid(): 
            emails=form.cleaned_data['emails']
            emails=emails.split(',')
            for e in emails:
                e=e.strip()
                i=Invitation(email=e, key=generate_key())
                i.save()
                u, created=User.objects.get_or_create(username=e[:30], email=e)
                notification.send([u], 'invite', {'key': i.key,
                                                     'profile':profile })
            
            
            if len(emails):
                messages.info(request, '%d invitation(s) has been sent ' % len(emails)) 
                    
            return redirect('homepage', code=code)
    else:
        form=InvitationForm(initial={'key':code})
            
    return render_to_response('researchers/invite.html', {'profile':profile, 'form':form, 'key':code}, context_instance=RequestContext(request))

def join(request, code):
    """ 
        TODO: After registring a user invitation should be disable.
    """
    if not check_invitation(code):
        messages.error(request, 'Your personal URL is incorrect, please ask for new invitation or provide proper url')
        return redirect('index')

    from forms import JoinForm
    if request.method == 'POST':
        form = JoinForm(request.POST) 
        if form.is_valid():
            profile=Profile(first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            unit=form.cleaned_data['unit'],
                            email=form.cleaned_data['email'],
                            key=generate_key())
            profile.save()
            keywords = __to_keywords(form.cleaned_data['keywords'])
            profile.keywords.clear();
            for k in keywords:
                profile.keywords.add(k)
            profile.save()

            return redirect('homepage', code=profile.key 
                            )
    else:
        form = JoinForm(initial={'key':code}) 
    
    return render_to_response('researchers/join.html', {
                              'form': form,
                              'key':code,  # invitation code
                              },context_instance=RequestContext(request))
    
    return render_to_response('researchers/join.html', {'form':form}, context_instance=RequestContext(request))


def update(request, code):
    profile = check_profile(code)
    if not profile:
        messages.error(request, 'Your personal URL is incorrect, please reset your account or provide proper url')
        return redirect('index', m='Your invitation URL is not valid')

    from forms import JoinForm

    if request.method == 'POST':
        form=JoinForm(request.POST)
        if form.is_valid():
            profile.first_name=form.cleaned_data['first_name']
            profile.last_name=form.cleaned_data['last_name']
            profile.unit=form.cleaned_data['unit']
            profile.email=form.cleaned_data['email']
            profile.save()
            keywords = __to_keywords(form.cleaned_data['keywords'])
            profile.keywords.clear();
            for k in keywords:
                profile.keywords.add(k)
            profile.save()
            messages.info(request, 'Your profile has been updated')
            return redirect(homepage, code=code)

    keywords=profile.summary()
    form=JoinForm(initial={
              'first_name':profile.first_name,
              'last_name':profile.last_name,                  
              'unit':profile.unit,
              'email':profile.email,
              'key':code,
              'keywords':keywords})
    return render_to_response('researchers/update.html', {'profile':profile, 'form':form,
                                                            'key':code}, 
                              context_instance=RequestContext(request))

def comment(request, code=''):
    if request.method == 'POST':
        content = request.POST.get('comment', None)
        if content:
            c=Comment(content=content, 
                      name=request.POST.get('name',''),
                      email=request.POST.get('email',''),
                      key=request.POST.get('key',''))
            c.save()
            messages.info(request, 'Thank you for your feedback.')
        else:
            messages.warning(request, "We don't accept feedback without content.")

    path = request.POST.get('path',reverse(index))
    return HttpResponseRedirect(path)
    