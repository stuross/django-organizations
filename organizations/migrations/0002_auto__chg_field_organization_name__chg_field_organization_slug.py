# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings
from organizations.models import get_user_model


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Organization.name'
        db.alter_column('organizations_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Organization.slug'
        db.alter_column('organizations_organization', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100))

    def backwards(self, orm):

        # Changing field 'Organization.name'
        db.alter_column('organizations_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Organization.slug'
        db.alter_column('organizations_organization', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

    models = {
        'organizations.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['{model}']".format(model=AUTH_USER_MODEL), 'through': "orm['organizations.OrganizationUser']", 'symmetrical': 'False'})
        },
        'organizations.organizationowner': {
            'Meta': {'object_name': 'OrganizationOwner'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owner'", 'unique': 'True', 'to': "orm['organizations.Organization']"}),
            'organization_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owned_organization'", 'unique': 'True', 'to': "orm['organizations.OrganizationUser']"})
        },
        'organizations.organizationuser': {
            'Meta': {'ordering': "['organization', 'user']", 'unique_together': "(('user', 'organization'),)", 'object_name': 'OrganizationUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_users'", 'to': "orm['organizations.Organization']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_users'", 'to': "orm['{model}']".format(model=AUTH_USER_MODEL)})
        }
    }

    complete_apps = ['organizations']
