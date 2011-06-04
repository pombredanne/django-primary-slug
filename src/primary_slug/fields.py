# -*- coding: utf-8 -*-
#
#  This file is part of django-primary-cms.
#
#  DESCRIPTION_DESCRIPTION_DESCRIPTION
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-primary-cms
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-primary-cms
#
#  Copyright 2011 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from django.db.models.fields import SlugField

from primary_cms import settings



class PrimarySlugField(SlugField):
    """
    Slugfield
    """
    
    def __init__(self, *args, **kwargs):
        super(PrimarySlugField, self).__init__(*args, **kwargs)
        
        self.populate_from = kwargs.pop('populate_from', None)
        
        self.slugify = kwargs.pop('slugify', slugify)
        assert hasattr(self.slugify, '__call__')
    
    def pre_save(self, instance, add):

        # get currently entered slug
        value = self.value_from_object(instance)

        # autopopulate
        if self.populate_from and not value:
            value = get_prepopulated_value(self, instance)

        slug = self.slugify(value)

        #if not slug:
        #    # no incoming value,  use model name
        #    slug = instance._meta.module_name

        slug = utils.crop_slug(self, slug)

        # ensure the slug is unique (if required)
        if self.unique or self.unique_with:
            slug = utils.generate_unique_slug(self, instance, slug)

        assert slug, 'value is filled before saving'

        # make the updated slug available as instance attribute
        setattr(instance, self.name, slug)

        return slug

def get_prepopulated_value(field, instance):
    """
    Returns preliminary value based on `populate_from`.
    """
    if hasattr(field.populate_from, '__call__'):
        # AutoSlugField(populate_from=lambda instance: ...)
        return field.populate_from(instance)
    else:
        # AutoSlugField(populate_from='foo')
        attr = getattr(instance, field.populate_from)
        return callable(attr) and attr() or attr

def crop_slug(field, slug):
    if field.max_length < len(slug):
        return slug[:field.max_length]
    return slug

