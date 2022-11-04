from rest_framework import permissions
from nacl.signing import VerifyKey
from solana.publickey import PublicKey
from reviewers.settings import SOLSCAN_API_HOLDERS, SOLSCAN_API, CREATOR
import time, base58, requests, json


class VerifyRequest(permissions.BasePermission):
    def _checkTime(self, timestamp):
        if timestamp + 300 < time.time():
            return False
        return True

    def _checkSignature(self, signature, timestamp, publicKey):
        pubkey = bytes(PublicKey(publicKey))
        msg = bytes(str(timestamp), 'utf8')
        signed = bytes(signature)

        result = VerifyKey(
            pubkey
        ).verify(
            smessage=msg,
            signature=base58.b58decode(signed)
        )

        return result

    def _checkNFT(self, publicKey, tokenAddress):
        holders = json.loads(requests.get(SOLSCAN_API_HOLDERS + tokenAddress).text)
        tokenMetadata = json.loads(requests.get(SOLSCAN_API + tokenAddress).text)
        symbol = tokenMetadata['data']['tokenInfo']['symbol']
        creators = [address['address'] for address in tokenMetadata['data']['metadata']['data']['creators']]
        isOwner = publicKey in [holder['owner'] for holder in holders['data']]
        metadataLink = tokenMetadata['data']['metadata']['data']['uri']
        isActive = json.loads(requests.get(metadataLink).text)['']

        # TODO: isActive

        if symbol == 'Rev' and CREATOR in creators and isOwner:
            return True
        return False

    def has_permission(self, request, view):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        publicKey = request.GET.get('publicKey')
        tokenAddress = request.GET.get('tokenAddress')

        try:
            if self._checkNFT(publicKey, tokenAddress) and self._checkSignature(signature, timestamp,
                                                                                publicKey) and self._checkTime(
                    timestamp):
                return True
            return False
        except Exception as e:
            return False
