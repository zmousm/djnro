# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Removing M2M table for field org_name on 'Institution'
        db.delete_table('edumanage_institution_org_name')
    
    
    def backwards(self, orm):
        
        # Adding M2M table for field org_name on 'Institution'
        db.create_table('edumanage_institution_org_name', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('institution', models.ForeignKey(orm['edumanage.institution'], null=False)),
            ('name_i18n', models.ForeignKey(orm['edumanage.name_i18n'], null=False))
        ))
        db.create_unique('edumanage_institution_org_name', ['institution_id', 'name_i18n_id'])
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'edumanage.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'contact_email'"}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'contact_firstname'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'contact_lastname'"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'contact_phone'"})
        },
        'edumanage.institution': {
            'Meta': {'object_name': 'Institution'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'realmid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Realm']"})
        },
        'edumanage.institutiondetails': {
            'Meta': {'object_name': 'InstitutionDetails'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'contact': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Contact']", 'symmetrical': 'False'}),
            'ertype': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1', 'db_column': "'type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['edumanage.Institution']", 'unique': 'True'}),
            'number_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '6'}),
            'number_user': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '6'}),
            'oper_name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.URL_i18n']", 'symmetrical': 'False'})
        },
        'edumanage.instrealm': {
            'Meta': {'object_name': 'InstRealm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'proxyto': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.InstServer']", 'symmetrical': 'False'}),
            'realmexpr': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'edumanage.instrealmmon': {
            'Meta': {'object_name': 'InstRealmMon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'mon_type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'realm': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'edumanage.instserver': {
            'Meta': {'object_name': 'InstServer'},
            'acct_port': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'ertype': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1', 'db_column': "'type'"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'proto': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'retry': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'edumanage.monlocaleapoldata': {
            'Meta': {'object_name': 'MonLocalEAPOLData'},
            'cert': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'eap_method': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'exp_response': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrealmmonid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.InstRealmMon']"}),
            'passwp': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_column': "'pass'"}),
            'phase2': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'edumanage.monproxybackclient': {
            'Meta': {'object_name': 'MonProxybackClient'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrealmmonid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.InstRealmMon']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'proto': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'edumanage.name_i18n': {
            'Meta': {'object_name': 'Name_i18n'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'edumanage.realm': {
            'Meta': {'object_name': 'Realm'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'contact': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Contact']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Name_i18n']", 'symmetrical': 'False'}),
            'stype': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.URL_i18n']", 'symmetrical': 'False'})
        },
        'edumanage.realmdata': {
            'Meta': {'object_name': 'RealmData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_IdP': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'number_IdPSP': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'number_SP': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'number_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9'}),
            'number_inst': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'number_user': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9'}),
            'realmid': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['edumanage.Realm']", 'unique': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {})
        },
        'edumanage.serviceloc': {
            'AP_no': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'IPv6': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'Meta': {'object_name': 'ServiceLoc'},
            'NAT': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'SSID': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'contact': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Contact']", 'symmetrical': 'False'}),
            'enc_level': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutionid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6'}),
            'loc_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Name_i18n']", 'symmetrical': 'False'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6'}),
            'port_restrict': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'transp_proxy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.URL_i18n']", 'symmetrical': 'False'}),
            'wired': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'edumanage.url_i18n': {
            'Meta': {'object_name': 'URL_i18n'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '180', 'db_column': "'URL'"}),
            'urltype': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'type'"})
        }
    }
    
    complete_apps = ['edumanage']
