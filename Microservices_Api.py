from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from translate import Translate

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class Services(Resource):
    parser.add_argument('input_uri', type=str, help='URI of Json File')
    parser.add_argument('lang', type=str, help='Give Target Language')
    parser.add_argument('output_uri', type=str, help='Destination URI to save the updated json')

    def __init__(self):
        self.input_url = None
        self.inp = None
        self.inp_file = None
        self.inp_b_name = None
        self.lang = None
        self.output_url = None
        self.out = None
        self.out_b_name = None
        self.out_file = None

    def get(self):
        args = parser.parse_args()
        self.input_url = args.get('input_uri')
        self.inp = self.input_url.split('/')
        self.inp_file = self.inp[3]
        self.inp_b_name = self.inp[2]
        self.lang = args.get('lang')
        self.output_url = args.get('output_uri')
        self.out = self.output_url.split('/')
        self.out_b_name = self.out[2]
        self.out_file = self.out[3]
        print(args)

        tran = Translate(in_file=self.inp_file, lang=self.lang, in_b_name=self.inp_b_name,
                         out_file=self.out_file, out_b_name=self.out_b_name)
        res = tran.download_aws()
        resp = tran.google_translate()
        respo = tran.upload_aws()
        data = {"status": 0, "info": ""}
        if res and resp and respo:
            data["status"] = 201
            data["info"] = "Successful Translation"
        else:
            data["status"] = 400
            data["info"] = "Failure at Somepoint"

        return jsonify(data)


api.add_resource(Services, '/translate/')

if __name__ == '__main__':
    app.run(debug=True)