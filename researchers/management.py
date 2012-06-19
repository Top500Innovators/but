import but.settings as settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("remind", _("URL reminder"), _("This is But URL reminder"))
        notification.create_notice_type("invite", _("But invitation"), _("Check this out, but will help you find coworkers"))
    signals.post_syncdb.connect(create_notice_types, sender=notification)





