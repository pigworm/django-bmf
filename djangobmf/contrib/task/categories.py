#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory


class GoalCategory(BaseCategory):
    name = _('Goals')
    slug = "goals"


class TaskCategory(BaseCategory):
    name = _('Tasks')
    slug = "tasks"