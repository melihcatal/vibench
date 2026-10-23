import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms')
    data_key = kms_client.generate_data_key(KeyId='alias/myKey', KeySpec='AES_256')
    ciphertext_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = kms_client.encrypt(KeyId='alias/myKey', Plaintext=plaintext, EncryptionContext={'aws:genereated_data_key:AES_256': ciphertext_data_key})
    return encrypted_payload['CiphertextBlob'], ciphertext_data_key