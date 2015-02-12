# Copyright 2014 Ebay Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#
# Author: Vijayendra Bhamidipati <vbhamidipati@paypal.com>

import argparse
import logging
import traceback

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _

"""
    'lb-sslcert-create': lbssl.CreateLbSSLCert,
    'lb-sslcert-list': lbssl.ListLbSSLCert,
    'lb-sslcert-show': lbssl.ShowLbSSLCert,
    'lb-sslcert-delete': lbssl.DeleteLbSSLCert,
    'lb-sslcert-update': lbssl.UpdateLbSSLCert,

    'lb-sslcertchain-create': lbssl.CreateLbSSLCertChain,
    'lb-sslcertchain-list': lbssl.ListLbSSLCertChain,
    'lb-sslcertchain-show': lbssl.ShowLbSSLCertChain,
    'lb-sslcertchain-delete': lbssl.DeleteLbSSLCertChain,
    'lb-sslcertchain-update': lbssl.UpdateLbSSLCertChain,

    'lb-sslcertkey-create': lbssl.CreateLbSSLCertKey,
    'lb-sslcertkey-list': lbssl.ListLbSSLCertKey,
    'lb-sslcertkey-show': lbssl.ShowLbSSLCertKey,
    'lb-sslcertkey-delete': lbssl.DeleteLbSSLCertKey,
    'lb-sslcertkey-update': lbssl.UpdateLbSSLCertKey

    'lb-sslprofile-create': lbssl.CreateLbSSLProfile,
    'lb-sslprofile-list': lbssl.ListLbSSLProfile,
    'lb-sslprofile-show': lbssl.ShowLbSSLProfile,
    'lb-sslprofile-delete': lbssl.DeleteLbSSLProfile,
    'lb-sslprofile-update': lbssl.UpdateLbSSLProfile,

    'lb-vip-sslcert-associate': AssociateVipSSLCert,
    'lb-vip-sslcert-disassociate': lbssl.DisassociateVipSSLCert,
    'lb-vip-sslcert-association-list': lbssl.ListVipSSLCertAssociations,
    'lb-vip-sslcert-association-show': lbssl.ShowVipSSLCertAssociation,
"""

class CreateLbSSLProfile(neutronV20.CreateCommand):

    """ Creates an association between a vip and an SSL certificate"""

    resource = 'ssl_profile'
    log = logging.getLogger(__name__ + '.CreateLbSSLProfile')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL profile'))
        parser.add_argument(
            '--description',
            required=False,
            help=_('Description of the SSL profile'))
        parser.add_argument(
            '--cert-id',
            dest="cert_id",
            required=True,
            help=_('UUID of SSL certificate'))
        parser.add_argument(
            '--key-id',
            dest="key_id",
            required=True,
            help=_('UUID of SSL private key'))
        parser.add_argument(
            '--cert-chain-id',
            dest="cert_chain_id",
            required=False,
            help=_('UUID of SSL Cert chain id'))
        parser.add_argument(
            '--shared',
            action='store_true',
            help=_('Specifying --shared makes the ssl profile visible to all tenants'),
            default=argparse.SUPPRESS)

    def args2body(self, parsed_args):
        if not parsed_args.cert_chain_id:
            cert_chain_id = ''
        else:
            cert_chain_id = parsed_args.cert_chain_id

        if not parsed_args.description:
            description = ''
        else:
            description = parsed_args.description
        body = {'ssl_profile': {
            'name': parsed_args.name,
            'description': description,
            'cert_id': parsed_args.cert_id,
            'cert_chain_id': cert_chain_id,
            'key_id': parsed_args.key_id}
        }
        neutronV20.update_dict(parsed_args, body['ssl_profile'],
                               ['tenant_id', 'shared'])
        return body


class ListLbSSLProfile(neutronV20.ListCommand):

    """List all SSL profiles for v1 lbaas api."""

    resource = 'ssl_profile'
    log = logging.getLogger(__name__ + '.ListLbSSLProfile')
    list_columns = ['id', 'tenant_id', 'name', 'description', 'cert_id', 'cert_chain_id', 'key_id']
    pagination_support = True
    sorting_support = True

    def add_known_arguments(self, parser):
        pass

    def args2body(self, parsed_args):
        body = {'ssl_profile': {
            'name': parsed_args.name,
            'description': parsed_args.description,
            'cert_id': parsed_args.cert_id,
            'cert_chain_id': parsed_args.cert_chain_id,
            'key_id': parsed_args.key_id}}
        neutronV20.update_dict(parsed_args, body['ssl_profile'],
                               ['tenant_id'])
        return body


class DeleteLbSSLProfile(neutronV20.DeleteCommand):

    """Delete an SSL certificate key in v1 lbaas api."""

    resource = 'ssl_profile'
    log = logging.getLogger(__name__ + '.DeleteLbSSLProfile')

    def args2body(self, parsed_args):
        body = {'ssl_profile': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_profile'],
                               ['tenant_id'])
        return body


class ShowLbSSLProfile(neutronV20.ShowCommand):

    """Show an ssl certificate key in v1 lbaas api."""
    resource = 'ssl_profile'
    log = logging.getLogger(__name__ + '.ShowLbSSLProfile')

    def args2body(self, parsed_args):
        body = {'ssl_profile': {
            'name': parsed_args.name,
            'description': parsed_args.description,
            'cert_id': parsed_args.cert_id,
            'cert_chain_id': parsed_args.cert_chain_id,
            'key_id': parsed_args.key_id}}
        neutronV20.update_dict(parsed_args, body['ssl_profile'],
                               ['tenant_id'])
        return body


class UpdateLbSSLProfile(neutronV20.UpdateCommand):

    """Update an SSL certificate key for v1 LBaaS ssl."""

    resource = 'ssl_profile'
    log = logging.getLogger(__name__ + '.UpdateLbSSLProfile')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--description',
            required=False,
            help=_('Description of the SSL profile'))

    def args2body(self, parsed_args):
        body = {'ssl_profile': {
            'name': parsed_args.name,
            'key': parsed_args.key}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body

################
class CreateLbSSLCertKey(neutronV20.CreateCommand):

    """Create an SSL certificate key for v1 LBaaS ssl."""

    resource = 'ssl_certificate_key'
    log = logging.getLogger(__name__ + '.CreateLbSSLCertKey')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate key'))
        parser.add_argument(
            '--key',
            required=True,
            dest="key",
            help=_('Key of vip SSL certificate/cert chain association'))

    def args2body(self, parsed_args):
        body = {'ssl_certificate_key': {
            'name': parsed_args.name,
            'key': parsed_args.key}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body


class ListLbSSLCertKey(neutronV20.ListCommand):

    """List all SSL cert keys for v1 lbaas api."""

    resource = 'ssl_certificate_key'
    log = logging.getLogger(__name__ + '.ListLbSSLCertKey')
    list_columns = ['id', 'tenant_id', 'name']
    pagination_support = True
    sorting_support = True

    def add_known_arguments(self, parser):
        pass

    def args2body(self, parsed_args):
        body = {'ssl_certificate_key': {
            'name': parsed_args.name,
            'key': parsed_args.key}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body


class DeleteLbSSLCertKey(neutronV20.DeleteCommand):

    """Delete an SSL certificate key in v1 lbaas api."""

    resource = 'ssl_certificate_key'
    log = logging.getLogger(__name__ + '.DeleteLbSSLCertKey')

    def args2body(self, parsed_args):
        body = {'ssl_certificate_key': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body


class ShowLbSSLCertKey(neutronV20.ShowCommand):

    """Show an ssl certificate key in v1 lbaas api."""
    resource = 'ssl_certificate_key'
    log = logging.getLogger(__name__ + '.ShowLbSSLCertKey')

    def args2body(self, parsed_args):
        body = {'ssl_certificate_key': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body


class UpdateLbSSLCertKey(neutronV20.UpdateCommand):

    """Update an SSL certificate key for v1 LBaaS ssl."""

    resource = 'ssl_certificate_key'
    log = logging.getLogger(__name__ + '.UpdateLbSSLCertKey')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate key'))
        parser.add_argument(
            '--key',
            dest="key",
            required=True,
            help=_('Private key of SSL certificate association '))

    def args2body(self, parsed_args):
        body = {'ssl_certificate_key': {
            'name': parsed_args.name,
            'key': parsed_args.key}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_key'],
                               ['tenant_id'])
        return body


class CreateLbSSLCertChain(neutronV20.CreateCommand):

    """Create an SSL certificate chain for v1 LBaaS ssl."""

    resource = 'ssl_certificate_chain'
    log = logging.getLogger(__name__ + '.CreateLbSSLCertChain')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate chain'))
        parser.add_argument(
            '--cert-chain',
            required=True,
            dest="cert_chain",
            help=_('Content of SSL certificate chain/intermediate certificate'))

    def args2body(self, parsed_args):
        body = {'ssl_certificate_chain': {
            'name': parsed_args.name,
            'cert_chain': parsed_args.cert_chain}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_chain'],
                               ['tenant_id'])
        return body


class ListLbSSLCertChain(neutronV20.ListCommand):

    """List all SSL cert chains for v1 lbaas api."""

    resource = 'ssl_certificate_chain'
    log = logging.getLogger(__name__ + '.ListLbSSLCertChain')
    list_columns = ['id', 'tenant_id', 'name']
    pagination_support = True
    sorting_support = True

    def add_known_arguments(self, parser):
        pass

    def args2body(self, parsed_args):
        body = {'ssl_certificate_chain': {
            'name': parsed_args.name,
            'cert_chain': parsed_args.cert_chain}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_chain'],
                               ['tenant_id'])
        return body


class DeleteLbSSLCertChain(neutronV20.DeleteCommand):

    """Delete an SSL certificate chain in v1 lbaas api."""

    resource = 'ssl_certificate_chain'
    log = logging.getLogger(__name__ + '.DeleteLbSSLCertChain')

    def args2body(self, parsed_args):
        body = {'ssl_certificate_chain': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_chain'],
                               ['tenant_id'])
        return body


class ShowLbSSLCertChain(neutronV20.ShowCommand):

    """Show an ssl certificate chain in v1 lbaas api."""
    resource = 'ssl_certificate_chain'
    log = logging.getLogger(__name__ + '.ShowLbSSLCertChain')

    def args2body(self, parsed_args):
        body = {'ssl_certificate_chain': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_chain'],
                               ['tenant_id'])
        return body


class UpdateLbSSLCertChain(neutronV20.UpdateCommand):

    """Update an SSL certificate chain for v1 LBaaS ssl."""

    resource = 'ssl_certificate_chain'
    log = logging.getLogger(__name__ + '.UpdateLbSSLCertChain')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate chain'))
        parser.add_argument(
            '--cert-chain',
            dest="cert_chain",
            required=True,
            help=_('Content of SSL certificate chain/intermediate cert'))

    def args2body(self, parsed_args):
        body = {'ssl_certificate_chain': {
            'name': parsed_args.name,
            'cert_chain': parsed_args.cert_chain}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate_chain'],
                               ['tenant_id'])
        return body


class AssociateVipSSLCert(neutronV20.CreateCommand):

    """ Creates an association between a vip and an SSL certificate"""

    resource = 'vip_ssl_certificate_association'
    log = logging.getLogger(__name__ + '.AssociateVipSSLCert')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the VIP SSL certificate association'))
        parser.add_argument(
            '--vip-id',
            dest="vip_id",
            required=True,
            help=_('Id of the VIP'))
        parser.add_argument(
            '--ssl-profile-id',
            dest="ssl_profile_id",
            required=True,
            help=_('Id of the SSL profile'))

    def args2body(self, parsed_args):
        body = {'vip_ssl_certificate_association': {
            'name': parsed_args.name,
            'vip_id': parsed_args.vip_id,
            'ssl_profile_id': parsed_args.ssl_profile_id}
        }
        neutronV20.update_dict(parsed_args, body['vip_ssl_certificate_association'],
                               ['tenant_id'])
        return body


class DisassociateVipSSLCert(neutronV20.DeleteCommand):

    """ Removes an association between a vip and an SSL certificate, chain, and key"""
    resource = 'vip_ssl_certificate_association'
    log = logging.getLogger(__name__ + '.DisassociateVipSSLCert')

    def args2body(self, parsed_args):
        body = {'vip_ssl_certificate_association': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['vip_ssl_certificate_association'],
                               ['tenant_id'])
        return body


class CreateLbSSLCert(neutronV20.CreateCommand):

    """Create an SSL certificate for v1 LBaaS ssl."""

    resource = 'ssl_certificate'
    log = logging.getLogger(__name__ + '.CreateLbSSLCert')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate'))
        parser.add_argument(
            '--description',
            required=False,
            help=_('Description of the SSL certificate'))
        parser.add_argument(
            '--passphrase',
            required=False,
            help=_('passphrase for the SSL certificate'))
        parser.add_argument(
            '--certificate',
            required=True,
            help=_('Content of SSL certificate'))

    def args2body(self, parsed_args):
        body = {'ssl_certificate': {
            'name': parsed_args.name,
            'description': parsed_args.description,
            'passphrase': parsed_args.passphrase,
            'certificate': parsed_args.certificate}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate'],
                               ['tenant_id'])
        return body


class ListLbSSLCert(neutronV20.ListCommand):

    """List all SSL certs for v1 lbaas api."""

    resource = 'ssl_certificate'
    log = logging.getLogger(__name__ + '.ListLbSSLCert')
    list_columns = ['id', 'name', 'description', 'passphrase']
    pagination_support = True
    sorting_support = True

    def add_known_arguments(self, parser):
        pass

    def args2body(self, parsed_args):
        body = {'ssl_certificate': {
            'name': parsed_args.name,
            'description': parsed_args.description,
            'passphrase': parsed_args.passphrase,
            'certificate': parsed_args.certificate}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate'],
                               ['tenant_id'])
        return body


class DeleteLbSSLCert(neutronV20.DeleteCommand):

    """Delete an SSL certificate in v1 lbaas api."""

    resource = 'ssl_certificate'
    log = logging.getLogger(__name__ + '.DeleteLbSSLCert')

    def args2body(self, parsed_args):
        body = {'ssl_certificate': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate'],
                               ['tenant_id'])
        return body


class ShowLbSSLCert(neutronV20.ShowCommand):

    """Show an ssl certificate in v1 lbaas api."""
    resource = 'ssl_certificate'
    log = logging.getLogger(__name__ + '.ShowLbSSLCert')

    def args2body(self, parsed_args):
        body = {'ssl_certificate': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate'],
                               ['tenant_id'])
        return body


class UpdateLbSSLCert(neutronV20.UpdateCommand):

    """Update an SSL certificate for v1 LBaaS ssl."""

    resource = 'ssl_certificate'
    log = logging.getLogger(__name__ + '.UpdateLbSSLCert')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            required=True,
            help=_('Name of the SSL certificate'))
        parser.add_argument(
            '--description',
            required=True,
            help=_('Description of the SSL certificate'))
        parser.add_argument(
            '--passphrase',
            required=True,
            help=_('passphrase for the SSL certificate'))
        parser.add_argument(
            '--certificate',
            required=True,
            help=_('Content of SSL certificate'))

    def args2body(self, parsed_args):
        body = {'ssl_certificate': {
            'id': parsed_args.id,
            'name': parsed_args.name,
            'description': parsed_args.description,
            'passphrase': parsed_args.passphrase,
            'certificate': parsed_args.certificate}}
        neutronV20.update_dict(parsed_args, body['ssl_certificate'],
                               ['tenant_id'])
        return body


class ListVipSSLCertAssociations(neutronV20.ListCommand):

    """List all vip ssl cert associations for v1 lbaas api."""

    resource = 'vip_ssl_certificate_association'
    log = logging.getLogger(__name__ + '.ListVipSSLCertAssociations')
    list_columns = [
        'id',
        'name',
        'vip_id',
        'ssl_profile_id',
        'status',
        'status_description']
    pagination_support = True
    sorting_support = True

    def add_known_arguments(self, parser):
        pass

    # def args2body(self, parsed_args):
    #    body = {'vip_ssl_certificate_association': {
    #        'id': parsed_args.id,
    #        'vip_id': parsed_args.vip_id,
    #        'cert_id': parsed_args.cert_id,
    #        'status_description': parsed_args.status_description,
    #        'status' : parsed_args.status} }
    #    neutronV20.update_dict(parsed_args, body['vip_ssl_certificate_association'],
    #                           ['tenant_id'])
    #    return body


class ShowVipSSLCertAssociation(neutronV20.ShowCommand):

    """Show an vip ssl certificate association in v1 lbaas api."""
    resource = 'vip_ssl_certificate_association'
    log = logging.getLogger(__name__ + '.ShowVipSSLCertAssociation')

    def args2body(self, parsed_args):
        body = {'vip_ssl_certificate_association': {
            'id': parsed_args.id}}
        neutronV20.update_dict(parsed_args, body['vip_ssl_certificate_association'],
                               ['tenant_id'])
        return body
