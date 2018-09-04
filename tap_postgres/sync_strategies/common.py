import singer
from singer import  metadata
import tap_postgres.db as post_db
import sys
import simplejson as json

def send_schema_message(stream, bookmark_properties):
    s_md = metadata.to_map(stream['metadata'])
    if s_md.get((), {}).get('is-view'):
        key_properties = s_md.get((), {}).get('view-key-properties', [])
    else:
        key_properties = s_md.get((), {}).get('table-key-properties', [])

    schema_message = { 'type' : 'SCHEMA',
                       'stream' : post_db.calculate_destination_stream_name(stream, s_md),
                       'schema' : stream['schema'],
                       'key_properties' : key_properties,
                       'bookmark_properties': bookmark_properties}

    sys.stdout.write(json.dumps(schema_message, use_decimal=True) + '\n')
    sys.stdout.flush()
