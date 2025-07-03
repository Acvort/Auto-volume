# -> py -3.12 -m pip install pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- Настройки ---
SETTINGS = {
    "volume_variable_name": "[Script] system volume"  # Название глобальной переменной в Advanced Scene Switcher.
}

def script_description():
    return "Auto-Volume - Сохраните уровень системной громкости в глобальную переменную Advanced Scene Switcher.\n@ Автор: Acvort (Асворт)."

import obspython as obs
import traceback

previous_volume = None
def run():
    system_volume = get_system_volume()
    if system_volume is not None:
        system_volume = f"{system_volume * 100:.0f}"
        global previous_volume
        if system_volume != previous_volume and set_advss_variable(SETTINGS["volume_variable_name"], system_volume):
            previous_volume = system_volume
            return True
    return False

from comtypes import CLSCTX_ALL  
def get_system_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        system_volume = volume.GetMasterVolumeLevelScalar()
        return system_volume
    except Exception as e:
        traceback.print_exc()
        return None

def set_advss_variable(name, value):
    try:
        proc_handler = obs.obs_get_proc_handler()
        
        cd = obs.calldata_create()
        obs.calldata_set_string(cd, "name", name)
        obs.calldata_set_string(cd, "value", str(value))
        
        obs.proc_handler_call(proc_handler, "advss_set_variable_value", cd)
        
        success = obs.calldata_bool(cd, "success")
        
        obs.calldata_destroy(cd)
        return success
    except Exception as e:
        traceback.print_exc()
        return None