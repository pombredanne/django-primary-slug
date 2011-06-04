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
from django.core.urlresolvers import get_callable
from primary_slug import settings
from primary_slug import utils


default_slugify = get_callable(settings.PRIMARY_SLUG_SLUGIFY_FUNC)

class PrimarySlugField(SlugField):
    """
    Slugfield
    """
    
    def __init__(self, *args, **kwargs):
        super(PrimarySlugField, self).__init__(*args, **kwargs)
        
        self.populate_from = kwargs.pop('populate_from', None)
        
        self.slugify = kwargs.pop('slugify', default_slugify)
        assert hasattr(self.slugify, '__call__')
    
    def pre_save(self, instance, add):
        """Returns field's value just before saving."""
        
        # get currently entered slug
        slug = self.value_from_object(instance)

        # If no slug has been set and a ``populate_from`` field has been set,
        # generate a slug from the value of the ``populate_from`` field.
        if self.populate_from and not slug:
            populate_from_field_value = utils.get_prepopulated_value(self, instance)

            # Slugify value
            slug = self.slugify(populate_from_field_value)
    
            if slug:
                # Crop slug
                slug = utils.crop_slug(self, slug)
                # Make the slug available as instance attribute
                setattr(instance, self.name, slug)
        
        return slug

