import os.path

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# Get all permissions that the app is using
def get_permissions(path):
    try:
      app = apk.APK(path)
      permissions = app.get_permissions()
      #print(permissions)
      return permissions
    except Exception as e:
      print(e)

# This function will delete com.android. from the permission string
def prepare_permission_set(permission):
    return permission.split(".")[-1]




def get_permission_list(apkpath):
    dt_permission = ["MODIFY_AUDIO_SETTINGS", "CAMERA", "ACCESS_WIFI_STATE", "FLASHLIGHT", "DISABLE_KEYGUARD",
                     "USE_CREDENTIALS", "WRITE_CONTACTS", "ACCESS_CACHE_FILESYSTEM", "RECEIVE_MMS",
                     "ACCESS_LOCATION_EXTRA_COMMANDS", "CALL_PHONE", "WRITE_EXTERNAL_STORAGE", "ACCESS_COARSE_LOCATION",
                     "READ_PHONE_STATE", "GET_TASKS", "READ_CONTACTS", "CHECK_LICENSE", "BLUETOOTH_ADMIN",
                     "WRITE_INTERNAL_STORAGE", "KILL_BACKGROUND_PROCESSES", "WRITE_APN_SETTINGS", "WAKE_LOCK",
                     "INSTALL_PACKAGES", "C2D_MESSAGE", "RECORD_AUDIO", "RECEIVE_SMS", "BROADCAST_STICKY",
                     "CHANGE_NETWORK_STATE", "SEND_SMS", "SAMSUNG_TUNTAP", "CHANGE_WIFI_STATE", "ACCESS_NETWORK_STATE",
                     "READ_GSERVICES", "BLUETOOTH", "RECEIVE", "WRITE_SECURE_SETTINGS", "READ_USER_DICTIONARY",
                     "BROADCAST_BADGE", "INSTALL_SHORTCUT", "MAPS_RECEIVE", "SET_WALLPAPER", "WRITE_SMS",
                     "RECEIVE_BOOT_COMPLETED", "READ_PROFILE", "MANAGE_ACCOUNTS", "VIBRATE", "RECEIVE_WAP_PUSH",
                     "INTERNET", "GET_ACCOUNTS", "WRITE_SYNC_SETTINGS", "MOUNT_UNMOUNT_FILESYSTEMS", "RESTART_PACKAGES",
                     "UPDATE_APP_OPS_STATS", "READ_SMS", "READ_INTERNAL_STORAGE", "ACCESS_MTK_MMHW",
                     "READ_EXTERNAL_STORAGE", "READ_SYNC_SETTINGS", "AUTHENTICATE_ACCOUNTS", "SYSTEM_ALERT_WINDOW",
                     "READ", "CHANGE_CONFIGURATION", "UNINSTALL_SHORTCUT", "WRITE_SETTINGS",
                     "INTERACT_ACROSS_USERS_FULL", "WRITE", "READ_LOGS", "ACCESS_FINE_LOCATION", "READ_SETTINGS",
                     "BILLING"]
    error_list = []
    apkname_list = []
    dataset_list = []
    app_permissions = []
    try:
        # get app permissions
        app_permissions = get_permissions(apkpath)
        # print(app_permissions)

        # prepare permissions (Remove com.android)
        prepared_permissions = list(map(prepare_permission_set, app_permissions))
        # print(prepared_permissions, end="\n\n")

        # Create permission dataset list
        l = []
        for permision in dt_permission:
            if permision in prepared_permissions:
                l.append(1)
            else:
                l.append(0)
        # print(l, end="\n\n")

        dataset_list.append(l)

        # permission_list.append(app_permissions)
        apkname_list.append(apkpath.split("\\")[-1])

    except Exception as e:
        error_list.append(apkpath.split("\\")[-1])

    df_permission = list(dt_permission)

    dataset = pd.DataFrame(dataset_list, columns=df_permission)

    dataset.to_csv("APK_dataset.csv", index=False)



    # Return the permissions the app uses and numpy array of images to be used in CNN DL model
    return app_permissions, dataset


def get_api_calls_sequence():
    pass


def get_dex(apk_path):
    import zipfile
    filename = os.path.basename(apk_path)
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        zip_ref.extract("classes.dex","temp_dex")
        old_name = r'temp_dex/classes.dex'
        new_name = r'temp_dex/'+filename+'.dex'
        try:
            os.rename(old_name, new_name)
        except FileExistsError:
            print("File already Exists")
            print("Removing existing file")
            # skip the below code
            # if you don't' want to forcefully rename
            os.remove(new_name)
            # rename it
            os.rename(old_name, new_name)
            print('Done renaming a file')
    return new_name


#print(get_dex(r'E:\DL\Android_Malware_Classification\Benign\0a3ea75a962d2ac9919a5c66879b53827ba62ed8b8813e2c72bc8e1393f19e17.apk'))