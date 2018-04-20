import requests

from config import DHIS2_REPORTTABLES_URL, DHIS2_USERNAME, DHIS2_PASSWORD


def check_pivot_table_favorites(favorites):
    '''
    Calls DHIS2 reportTables API to check whether given favorite names
    exist or not

    Returns favorites that exist

    Eg:

    https://play.dhis2.org/2.29/api/reportTables.json
    ?filter=displayName:in:[testing_favorite_123,testing_favorite_s123]

    Result is:

    {
      "pager": {
        "page": 1,
        "pageCount": 1,
        "total": 2,
        "pageSize": 50
      },
      "reportTables": [
        {
          "id": "eoAyVSLOTEO",
          "displayName": "testing_favorite_123"
        },
        {
          "id": "H4NogjfKVC4",
          "displayName": "testing_favorite_s123"
        }
      ]
    }
    '''

    results = requests.get(DHIS2_REPORTTABLES_URL, params={
        'filter': 'displayName:in:[{}]'.format(','.join(favorites))
    }, auth=(DHIS2_USERNAME, DHIS2_PASSWORD))
    results.raise_for_status()
    results = results.json()['reportTables']

    return [r['displayName'] for r in results]
