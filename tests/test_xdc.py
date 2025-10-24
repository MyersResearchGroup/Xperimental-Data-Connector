import tricahue
import unittest
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# fj_url = "charmmefj-api.synbiohub.org"
fj_url = "127.0.0.1:8000"
fj_user = "test"
fj_pass = "test123"

sbh_url = "https://synbiohub.org"
sbh_user = "test@test.test"
sbh_pass = "test123"
sbh_collec = "XDC_package_test"

test_file_path ='tests/test_files'
excel_path = os.path.join(test_file_path, 'Tricahue_v11.6b_Medias.xlsx')

homespace = 'https://synbiohub.org/synbiotest'

fj_overwrite = False
sbh_overwrite = False

# xdc = tricahue.XDC(input_excel_path = excel_path,
#             fj_url = fj_url,
#             fj_user = fj_user, 
#             fj_pass = fj_pass, 
#             sbh_url = sbh_url, 
#             sbh_user = sbh_user, 
#             sbh_pass = sbh_pass, 
#             sbh_collection = sbh_collec, 
#             sbh_collection_description = 'Tricahue XDC package test collection',
#             sbh_overwrite = sbh_overwrite, 
#             fj_overwrite = fj_overwrite, 
#             homespace = homespace,
#             fj_token = None, 
#             sbh_token = None)

class Test_XDC(unittest.TestCase):
    def setup(self, filename, extension):
        # TODO: get file path so it can be run from anywhere
        excel_path = os.path.join(test_file_path, filename+'.'+extension)
        self.xdc = tricahue.XDC(input_excel_path = excel_path,
            fj_url = fj_url,
            fj_user = fj_user, 
            fj_pass = fj_pass, 
            sbh_url = sbh_url, 
            sbh_user = sbh_user, 
            sbh_pass = sbh_pass, 
            sbh_collection = filename + '_test', 
            sbh_collection_description = filename + ' test collection description',
            sbh_overwrite = sbh_overwrite,
            fj_overwrite = fj_overwrite, 
            homespace = homespace,
            fj_token = None, 
            sbh_token = None)

    def test_medias(self):
        # make this part of the unittest setup method
        self.setup('Tricahue_v11.6b_Medias', 'xlsx')
        self.xdc.initialize()
        self.xdc.log_in_sbh()
        sbh_token = self.xdc.sbh_token
        # print(sbh_token)
        response = requests.get('https://synbiohub.org/user/synbiotest/Tricahue_v11.6b_Medias_test/Tricahue_v11.6b_Medias_collection/1/removeCollection',
                        headers={
                            'Accept': 'text/plain',
                            'X-authorization': sbh_token},)
        print(response.status_code)
        if response.status_code == 403:
            print("Collection does not already exist, continue with test")

        self.xdc.log_in_fj()

        self.xdc.convert_to_sbol()
        self.xdc.generate_sbol_hash_map()
        
        self.xdc.upload_to_fj()
        self.xdc.upload_to_sbh()

        # requests.get something from collection and assertEquals status 200
        response = requests.get('https://synbiohub.org/user/synbiotest/Tricahue_v11.6b_Medias_test/Tricahue_v11.6b_Medias_collection/1/',
                        headers={
                            'Accept': 'text/plain',
                            'X-authorization': sbh_token},)
        assert response.status_code == 200

    @unittest.skip("chassis test")
    def test_chassis(self):
        # response = requests.get('<URI>/removeCollection',
        #                         headers={
        #                             'Accept': 'text/plain',
        #                             'X-authorization': '<token>'},)
        # print(response.status_code)
        self.setup('Tricahue_v11.6b_Chassis', 'xlsx')
        self.xdc.run()

    @unittest.skip('hi')
    def test_chemicals(self):
        # response = requests.get('<URI>/removeCollection',
        #                         headers={
        #                             'Accept': 'text/plain',
        #                             'X-authorization': '<token>'},)
        # print(response.status_code)
        self.setup('Tricahue_v11.6b_Chemicals', 'xlsx')
        self.xdc.run()

    @unittest.skip("bruh")
    def test_strain(self):
        # response = requests.get('<URI>/removeCollection',
        #                         headers={
        #                             'Accept': 'text/plain',
        #                             'X-authorization': '<token>'},)
        # print(response.status_code)
        self.setup('Tricahue_Strain', 'xlsx')
        self.xdc.run()
        
if __name__ == '__main__':
    unittest.main()
