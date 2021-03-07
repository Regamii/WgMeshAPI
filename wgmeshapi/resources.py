from wgmeshapi import api, db
from wgmeshapi.models import Netaddr, Peer
from wgmeshapi.wireguard import WireGuard as wg
from flask_restful import Resource, reqparse

NetworkAddressesParser = reqparse.RequestParser()
NetworkAddressesParser.add_argument('description', required=True, type=str, help='Description to this network')
NetworkAddressesParser.add_argument('netaddr', required=True, type=str, help='Virtual network address to use')

PeersParser = reqparse.RequestParser()
PeersParser.add_argument('name', required=True, type=str, help='Name of the peer')
PeersParser.add_argument('address', required=True, type=str, help='IP address in the overlay network')
PeersParser.add_argument('endpoint', required=True, type=str, help='Endpoint in the \'normal\' network')
PeersParser.add_argument('privkey', required=False, type=str, help='Private key of this peer, auto-generated if not set')

class NetworkAddressesList(Resource):
    def get(self):
        results = Netaddr.query.all()
        netaddrs = {}
        for result in results:
            netaddrs[result.id] = {
                'description': result.description,
                'netaddr': result.netaddr
            }
        return netaddrs

    def post(self):
        args = NetworkAddressesParser.parse_args()
        netaddr = Netaddr(
            description=args['description'],
            netaddr=args['netaddr']
        )
        db.session.add(netaddr)
        try:
            db.session.commit()
        except Exception:
            return {'message': 'Resource not created.'}
        return {
            'id': netaddr.id,
            'description': netaddr.description,
            'netaddr': netaddr.netaddr
        }, 201


class NetworkAddresses(Resource):
    def get(self, id):
        result = Netaddr.query.get_or_404(id)
        return {
            'id': result.id,
            'description': result.description,
            'netaddr': result.netaddr
        }

    def put(self, id):
        args = NetworkAddressesParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)
        netaddr.description = args['description']
        netaddr.netaddr = args['netaddr']
        db.session.add(netaddr)
        try:
            db.session.commit()
            return {
                'id': netaddr.id,
                'description': netaddr.description,
                'netaddr': netaddr.netaddr
            }
        except Exception:
            return {'message': 'Resource not altered.'}

    def delete(self, id):
        netaddr = Netaddr.query.get_or_404(id)
        db.session.delete(netaddr)
        try:
            db.session.commit()
            return None, 204
        except Exception:
            return {'message': 'Resource not deleted.'}


class PeersList(Resource):
    def get(self, id):
        results = Netaddr.query.get_or_404(id).peers
        peers = {}
        for result in results:
            peers[result.id] = {
                'name': result.name,
                'address': result.address,
                'endpoint': result.endpoint,
                'privkey': result.privkey
            }
        return peers

    def post(arg, id):
        args = PeersParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)

        if args['privkey']:
            privkey = args['privkey']
        else:
            privkey = wg.genkey()

        peer = Peer(
            name=args['name'],
            netaddr_id=netaddr.id,
            address=args['address'],
            endpoint=args['endpoint'],
            privkey=privkey
        )

        db.session.add(peer)
        try:
            db.session.commit()
            peer = Peer.query.get(peer.id)
            return {
                'id': peer.id,
                'name': peer.name,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'privkey': peer.privkey
            }, 201
        except Exception:
            return {'message': 'Resource not created.'}


api.add_resource(NetworkAddressesList, '/netaddr')
api.add_resource(NetworkAddresses, '/netaddr/<int:id>')
api.add_resource(PeersList, '/netaddr/<int:id>/peer')