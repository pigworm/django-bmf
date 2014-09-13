#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


@python_2_unicode_compatible
class Workspace(MPTTModel):
    name = models.CharField(max_length=30, blank=False)
    slug = models.SlugField(max_length=30, blank=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        limit_choices_to={'level__lt': 2},
    )
    url = models.CharField(max_length=255, blank=False, editable=False, db_index=True)
    ct = models.ForeignKey(ContentType, related_name="+", on_delete=models.CASCADE, blank=True, null=True)

    public = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)

    label = models.CharField(max_length=100, blank=False, editable=False)
    plugin = models.CharField(max_length=100, blank=False, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Workspace")
        verbose_name_plural = _("Workspace")
        unique_together = (("parent", "slug"), )

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Workspace, self).__init__(*args, **kwargs)
        self.org = self.pk
        self.org_level = self.level

    def clean(self):
        if self.org:
            if (self.parent and self.parent.level != self.org_level - 1) or (not self.parent and self.org_level != 0):
                raise ValidationError(
                    'moveing between different types is not allowed',
                )
                
        if not self.parent:
            self.ct = None
        else:
            if self.parent.level == 2:
                raise ValidationError(
                    'You are not allowed to append to this type',
                )
            if self.parent.level == 1 and not self.ct:
                raise ValidationError(
                    'You need to define a ContentType',
                )
            if self.parent.level == 0:
                self.ct = None
        self.update_url()

    def save(self, *args, **kwargs):
        super(Workspace, self).save(*args, **kwargs)
        qs = self.get_descendants()
        for workspace in qs:
            workspace.update_url()
            workspace.save()

    def type(self):
        if self.level == 2:
            return _('View')
        elif self.level == 1:
            return _('Category')
        return _('Workspace')

    def update_url(self):
         if self.parent:
             self.url = "%s/%s" % (self.parent.url, self.slug)
         else:
             self.url = self.slug