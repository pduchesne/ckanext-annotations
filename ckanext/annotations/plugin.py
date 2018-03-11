import requests
import ckan.plugins as p
import json
import urllib2
import urllib
import simplejson

from ckan.logic import get_action
from ckan import model
from logging import getLogger
from pylons import config
import ckan.lib.helpers as h

try:
    from ckan.lib.datapreview import on_same_domain
except ImportError:
    from ckan.lib.datapreview import _on_same_domain as on_same_domain

log = getLogger(__name__)

class AnnotationPlugin(p.SingletonPlugin):
    """This plugin hooks in when a data package has been added.
       The resulting package will be investigated for Annotations from the configured Annotation Server.
    """

    # inheriting from IDomainObjectModification makes sure that we get notifications about updates with resources
    #p.implements(p.IDomainObjectModification)
    # IConfigurable makes sure we can reuse the config class
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer, inherit=True)
    if p.toolkit.check_ckan_version(min_version='2.3'):
        p.implements(p.IResourceView, inherit=True)
    else:
        p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    proxy_enabled = False
    same_domain = False

    def configure(self, config):
        self.mosaics_user = config.get("mosaics.user","admin")
        self.mosaics_pass = config.get("mosaics.pass","admin")
        self.mosaics_server_url = config.get("mosaics.server_url","http://localhost/api")


    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('public', 'ckanext-annotations')

        self.proxy_enabled = 'resource_proxy' in config.get('ckan.plugins', '')

    '''
    def notify(self, entity, operation=None):
        # Make sure we're working with a Resource
        if isinstance(entity, model.Resource):
            if operation:
                if operation == model.domain_object.DomainObjectOperation.deleted:
                    self.delete_tdt_source(entity)
                else:
                    self.create_tdt_source(entity)
        return
    '''

    def info(self):
        return {'name': 'annotations',
                'title': 'Annotations',
                'icon': 'comments',
                'iframed': False,
                'default_title': p.toolkit._('Annotations'),
                'schema': {},
                }

    def can_view(self, data_dict):
        format_lower = data_dict['resource'].get('format', '').lower()
        same_domain = on_same_domain(data_dict)

        # Guess from file extension
        if not format_lower and data_dict['resource'].get('url'):
            format_lower = self._guess_format_from_extension(
                data_dict['resource']['url'])

        ''' TODO implement format validation depending on supported formats server-side
        view_formats = config.get('ckanext.geoview.ol_viewer.formats', '')
        if view_formats:
            view_formats.split(' ')
        else:
            view_formats = MOSAICS_FORMATS

        correct_format = format_lower in view_formats
        '''

        # TODO use local proxy to lower charge on mosaics server
        # for now simply redirect everything to mosaics server
        can_preview_from_domain = True # self.proxy_enabled or same_domain

        return can_preview_from_domain #and correct_format

    def view_template(self, context, data_dict):
        return 'annotations/mosaics.html'


    # IResourcePreview (CKAN < 2.3)

    def can_preview(self, data_dict):

        return self.can_view(data_dict)

    def preview_template(self, context, data_dict):
        return 'annotations/mosaics.html'

    def setup_template_variables(self, context, data_dict):
        p.toolkit.c.jsondump = json.dumps
        p.toolkit.c.mosaics_server_url = self.mosaics_server_url
        p.toolkit.c.id = data_dict["resource"]["id"]
        p.toolkit.c.name = data_dict["resource"]["name"]
        p.toolkit.c.url = data_dict["resource"]["url"]


    def get_helpers(self):
        return {
            'jsondump' : json.dumps,
            'urlencode' : urllib.quote_plus
        }

