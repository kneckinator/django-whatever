# -*- coding: utf-8 -*-
from inspect import isfunction, ismethod
import django
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import ForeignKey, OneToOneField
from django_any.models import any_model


def any_model_with_defaults(cls, **attrs):
    """Use model-provided defaults"""

    for field in cls._meta.fields:
        default = field.default
        if default is not NOT_PROVIDED:
            if isfunction(default) or ismethod(default):
                # for stuff like default=datetime.now
                default = default()
            if isinstance(field, (ForeignKey, OneToOneField)):
                if django.VERSION >= (1, 9):
                    Model = field.target_field.model
                else:
                    Model = field.related_field.model
                if not isinstance(default, Model):
                    try:
                        default = Model.objects.get(pk=default)
                    except Model.DoesNotExist:
                        pass
            attrs.setdefault(field.name, default)

    return any_model(cls, **attrs)
