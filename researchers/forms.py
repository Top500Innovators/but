# coding: utf-8
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

class InvitationForm(forms.Form):
    emails=forms.CharField(label=_('Emails'),widget=widgets.Textarea(attrs={'size':'255', 
                                                                     'onKeyDown':"textCounter(document.form.id_emails,document.form.id_counter,255)",
                                                                     'onKeyUp':"textCounter(document.form.id_emails,document.form.id_counter,255)"}), required=True)

class ResetKeyForm(forms.Form):
    email=forms.EmailField(label=_('Email'),required=True)


class JoinForm(forms.Form):
    first_name=forms.CharField(label=_('First name'),initial='',required=True)
    last_name=forms.CharField(label=_('Last name'),initial='',required=True)
    unit=forms.CharField(label=_('Unit'),initial='',required=True)
    email=forms.EmailField(label=_('Email'),initial='',required=True)
    keywords=forms.CharField(label=_('Keywords (e.g.: mathematician, programmer)'),
                             widget=widgets.Textarea(attrs={'size':'255', 
                                                            'onKeyDown':"textCounter(document.form.id_keywords,document.form.id_counter,255)",
                                                            'onKeyUp':"textCounter(document.form.id_keywords,document.form.id_counter,255)"}), 
                                    required=True)
    key=forms.CharField(widget=widgets.HiddenInput(),required=True)

class SearchForm(forms.Form):
    search=forms.CharField(label=_('keywords'),
                                initial='',
                                required=True, 
                                widget=forms.TextInput(attrs={'size':'50', 
                                                                'onKeyDown':"textCounter(document.form.id_search,document.form.id_counter,50)",
                                                                'onKeyUp':"textCounter(document.form.id_search,document.form.id_counter,50)"}))
