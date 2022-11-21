from rest_framework import permissions
from nacl.signing import VerifyKey
from solana.publickey import PublicKey
from reviewers.settings import SOLSCAN_API, CREATOR, SOLSCAN_API_TOKENS
import time, base58, requests, json
from utils.stuff import PrintException

class VerifyRequest(permissions.BasePermission):
    def _checkTime(self, timestamp):
        print(int(timestamp)+60000, time.time(), int(timestamp) + 60000 < time.time())
        if int(timestamp) + 60000 < time.time():
            return False
        return True

    def _checkSignature(self, signature, timestamp, publicKey):
        print(4)
        pubkey = bytes(PublicKey(publicKey))
        msg = bytes(str(timestamp), 'utf8')

        result = VerifyKey(
            pubkey
        ).verify(
            smessage=msg,
            signature=base58.b58decode(signature)
        )
        print(5)
        print(result)
        return result

    def _checkNFT(self, publicKey):
        print(2)
        tokens = json.loads(requests.get(SOLSCAN_API_TOKENS + publicKey).text)['data']
        tokenAddress = [token['tokenAddress'] for token in tokens if token['tokenSymbol'] == 'Rev']
        tokenAddress = tokenAddress[0]
        tokenMetadata = json.loads(requests.get(SOLSCAN_API + tokenAddress).text)
        creators = [address['address'] for address in tokenMetadata['data']['metadata']['data']['creators']]
        metadataLink = tokenMetadata['data']['metadata']['data']['uri']

        # isActive = json.loads(requests.get(metadataLink).text)['']
        # TODO: isActive
        print(3)
        if CREATOR in creators:
            return True
        return False

    def has_permission(self, request, view):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        publicKey = request.GET.get('publicKey')

        print(1)

        try:
            if self._checkNFT(publicKey) and self._checkSignature(signature, timestamp,
                                                                  publicKey) and self._checkTime(
                timestamp):
                return True
            return False
        except Exception as e:
            PrintException()
            print(e)
            return False

