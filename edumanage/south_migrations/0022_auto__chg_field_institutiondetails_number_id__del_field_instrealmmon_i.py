# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'InstitutionDetails.number_id'
        db.alter_column('edumanage_institutiondetails', 'number_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=6, null=True, blank=True))

        # Deleting field 'InstRealmMon.instid'
        db.delete_column('edumanage_instrealmmon', 'instid_id')

        # Renaming column for 'InstRealmMon.realm' to match new field type.
        db.rename_column('edumanage_instrealmmon', 'realm', 'realm_id')
        # Changing field 'InstRealmMon.realm'
        # WORKAROUND NEEDED
        # This migration breaks with PostgreSQL with:
        #   ERROR:  column "realm_id" cannot be cast automatically to type integer
        #   HINT:  Specify a USING expression to perform the conversion.
        #   STATEMENT:  ALTER TABLE "edumanage_instrealmmon" ALTER COLUMN "realm_id" TYPE integer,
        #          ALTER COLUMN "realm_id" SET NOT NULL, ALTER COLUMN "realm_id" DROP DEFAULT;
        # This is a known problem: http://south.aeracode.org/ticket/484
        # (PostgreSQL will not automatically convert and conversion must be provided with the USING clause)
        # Workaround: For PostgreSQL invoke a direct SQL statement amended with a USING clause to do the converion explicitly.
        # Credits:
        # * http://codeinthehole.com/writing/altering-postgres-table-columns-with-south/
        # * http://stackoverflow.com/questions/13170570/change-type-of-varchar-field-to-integer-cannot-be-cast-automatically-to-type-i
        if ( db._get_connection().vendor == "postgresql" ):
            db.execute('ALTER TABLE "edumanage_instrealmmon" ALTER COLUMN "realm_id" TYPE integer USING (trim(realm_id)::integer),'
                    ' ALTER COLUMN "realm_id" SET NOT NULL,'
                    ' ALTER COLUMN "realm_id" DROP DEFAULT,'
                    ' ADD CONSTRAINT "edumanage_i_realm_id_24cc89d4be4145e5_fk_edumanage_instrealm_id" FOREIGN KEY (realm_id) REFERENCES edumanage_instrealm(id) DEFERRABLE INITIALLY DEFERRED;')
        else:
            db.alter_column('edumanage_instrealmmon', 'realm_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['edumanage.InstRealm']))

        # Adding index on 'InstRealmMon', fields ['realm']
        db.create_index('edumanage_instrealmmon', ['realm_id'])

        # Changing field 'InstRealmMon.mon_type'
        db.alter_column('edumanage_instrealmmon', 'mon_type', self.gf('django.db.models.fields.CharField')(max_length=16))
    
    
    def backwards(self, orm):
        
        # Changing field 'InstitutionDetails.number_id'
        db.alter_column('edumanage_institutiondetails', 'number_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=6))

        # Adding field 'InstRealmMon.instid'
        db.add_column('edumanage_instrealmmon', 'instid', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['edumanage.Institution']), keep_default=False)

        # Renaming column for 'InstRealmMon.realm' to match new field type.
        db.rename_column('edumanage_instrealmmon', 'realm_id', 'realm')
        # Changing field 'InstRealmMon.realm'
        db.alter_column('edumanage_instrealmmon', 'realm', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Removing index on 'InstRealmMon', fields ['realm']
        db.delete_index('edumanage_instrealmmon', ['realm_id'])

        # Changing field 'InstRealmMon.mon_type'
        db.alter_column('edumanage_instrealmmon', 'mon_type', self.gf('django.db.models.fields.CharField')(max_length=8))
    
    
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'contact_name'"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'contact_phone'"})
        },
        'edumanage.institution': {
            'Meta': {'object_name': 'Institution'},
            'ertype': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1', 'db_column': "'type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'realmid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Realm']"})
        },
        'edumanage.institutioncontactpool': {
            'Meta': {'object_name': 'InstitutionContactPool'},
            'contact': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['edumanage.Contact']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"})
        },
        'edumanage.institutiondetails': {
            'Meta': {'object_name': 'InstitutionDetails'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'contact': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.Contact']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['edumanage.Institution']", 'unique': 'True'}),
            'number_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'number_user': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'oper_name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'edumanage.instrealm': {
            'Meta': {'object_name': 'InstRealm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'proxyto': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumanage.InstServer']", 'symmetrical': 'False'}),
            'realm': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        'edumanage.instrealmmon': {
            'Meta': {'object_name': 'InstRealmMon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mon_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'realm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.InstRealm']"})
        },
        'edumanage.instserver': {
            'Meta': {'object_name': 'InstServer'},
            'acct_port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1813', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'ertype': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1', 'db_column': "'type'"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1812', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'proto': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'retry': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
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
            'stype': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'contact': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumanage.Contact']", 'null': 'True', 'blank': 'True'}),
            'enc_level': ('edumanage.models.MultiSelectField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutionid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumanage.Institution']"}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6'}),
            'port_restrict': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'transp_proxy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wired': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'edumanage.url_i18n': {
            'Meta': {'object_name': 'URL_i18n'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '180', 'db_column': "'URL'"}),
            'urltype': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'type'"})
        }
    }
    
    complete_apps = ['edumanage']
