import configparser
import yaml
import requests


CFG_FILE = 'base.cfg'


class Overview(object):
    def __init__(self, cfg):
        self.root_url = cfg['base']['fhir_server']
        self.info = {}
        self.get_metadata()
        self.get_examples()

    def get(self, path):
        url = requests.compat.urljoin(self.root_url, path)
        response = requests.get(url)
        return response.json()

    def get_metadata(self):
        r = self.get('base/metadata?_format=json')
        resources = r['rest'][0]['resource']

        self.info['resources'] = {}
        for resource in resources:
            r_type = resource['type']
            r_params = []
            for param in resource.get('searchParam', []):
                r_params.append(param['name'])

            self.info['resources'][r_type] = {
                'searchParam': r_params,
            }

    def get_examples(self):
        self.info['examples'] = {}
        random_id = '5'
        for resource_type in self.info['resources']:
            example = self.get('base/{}/{}?_format=json'.format(resource_type, random_id))
            self.info['examples'][resource_type] = example


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read(CFG_FILE)
    overview = Overview(cfg)
    print(yaml.dump(overview.info, default_flow_style=False))
