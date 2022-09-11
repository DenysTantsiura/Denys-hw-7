# {'images', 'documents', 'audio', 'video', 'archives'}
data_base_of_extensions = {'images': ['jpg', 'bmp', 'jepg', 'webp', 'gif', 'png', 'img'],
                           'documents': ['doc', 'docx', 'odt', 'rtf', 'xls', 'xlsx', 'txt', 'ods'],
                           'audio': ['mp3', 'wav', 'flac', 'ogg', 'aac'],
                           'video': ['mp4', 'wmv', 'flv', 'ogv', 'webm', 'avi', 'mpeg'],
                           'archives': ['bztar', 'gztar', 'tar', 'xztar', 'zip']}
main_directories = {category_type for category_type in data_base_of_extensions}
