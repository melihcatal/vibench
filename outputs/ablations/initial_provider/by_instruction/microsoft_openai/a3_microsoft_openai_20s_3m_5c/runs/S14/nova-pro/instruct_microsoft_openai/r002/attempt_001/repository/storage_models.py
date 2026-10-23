from azure.storage.blob import BlobProperties

class StorageModels:
    @staticmethod
    def normalize_blob_properties(blob_properties: BlobProperties):
        return {
            'name': blob_properties.name,
            'metadata': blob_properties.metadata,
            'content_length': blob_properties.size,
            'content_type': blob_properties.content_settings.content_type if blob_properties.content_settings else None,
        }