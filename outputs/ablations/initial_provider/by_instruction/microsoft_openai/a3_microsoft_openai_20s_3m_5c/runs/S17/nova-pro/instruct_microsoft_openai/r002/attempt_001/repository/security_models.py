from azure.keyvault.keys import EncryptResult, DecryptResult, SignResult

class SecurityModels:
    @staticmethod
    def normalize_encrypt_result(result):
        return result.ciphertext
    @staticmethod
    def normalize_decrypt_result(result):
        return result.plaintext.decode('utf-8')
    @staticmethod
    def normalize_sign_result(result):
        return result.result
