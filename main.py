import dexBasedDL
import permissionBasedDL
import featureExtraction
import glob
import os

def main(args):

    app_permissions, dataset = featureExtraction.get_permission_list(args.apkpath)
    dex_file_path = featureExtraction.get_dex(args.apkpath)
    print(app_permissions)
    print(dex_file_path)

    permission_predictions = permissionBasedDL.predect_permission_based(dataset)
    dex_predictions,img_path = dexBasedDL.predect_dex_based(dex_file_path)

    print("prediction from permission based model:", permission_predictions)
    print("prediction from permission based model: (rounded)", permission_predictions.round())

    print("prediction from dex based model:", dex_predictions)
    print("prediction from dex based model: (rounded)", dex_predictions.round())
    ensimbled_prediction = [dex_predictions[0][0]*0.6+permission_predictions[0][0]*0.4, dex_predictions[0][1]*0.6+permission_predictions[0][1]*0.4]

    round_to_tenths = [round(num) for num in ensimbled_prediction]

    print("our estimated results: ",ensimbled_prediction)
    print("our estimated results: ",ensimbled_prediction, round_to_tenths)

if __name__ == '__main__':
    import argparse
    import glob

    parser = argparse.ArgumentParser(description='DruiDector - Deep Learning Android Malware detection')
    parser.add_argument('apkpath', metavar='apkpath', type=str,
                        help='Android APK file path to analyze')

    args = parser.parse_args()
    main(args)


def clean_files():
    del_files = glob.glob("temp_dex/*")
    for file in del_files:
        os.remove(file)


def flask_call(apk_path):
    app_permissions, dataset = featureExtraction.get_permission_list(apk_path)
    dex_file_path = featureExtraction.get_dex(apk_path)


    permission_predictions = permissionBasedDL.predect_permission_based(dataset)
    dex_predictions,img_path = dexBasedDL.predect_dex_based(dex_file_path)

    ensimbled_prediction = [dex_predictions[0][0]*0.6+permission_predictions[0][0]*0.4, dex_predictions[0][1]*0.6+permission_predictions[0][1]*0.4]

    round_to_tenths = [round(num) for num in ensimbled_prediction]

    print("our estimated results: ",ensimbled_prediction)
    print("our estimated results: ",ensimbled_prediction, round_to_tenths)
    clean_files()

    return app_permissions,permission_predictions, dex_predictions, ensimbled_prediction, round_to_tenths,img_path
