from Firefly import logging
from Firefly.components.zwave.device_types.switch import ZwaveSwitch
from Firefly.const import ACTION_OFF, ACTION_ON, SWITCH
from Firefly.services.alexa.alexa_const import ALEXA_SMARTPLUG

TITLE = 'Aeotec Smart Switch 6'

BATTERY = 'battery'
ALARM = 'alarm'
POWER_METER = 'power_meter'
VOLTAGE_METER = 'voltage_meter'

CURRENT = 'power_current'
CURRENT_ENERGY_READING = 'current_energy_reading'
PREVIOUS_ENERGY_READING = 'previous_energy_reading'
VOLTAGE = 'voltage'
WATTS = 'watts'

COMMANDS = [ACTION_OFF, ACTION_ON]
REQUESTS = [SWITCH, CURRENT, VOLTAGE, WATTS]

INITIAL_VALUES = {}

CAPABILITIES = {
  POWER_METER: True,
  SWITCH:      True,
}


def Setup(firefly, package, **kwargs):
  logging.message('Entering %s setup' % TITLE)
  switch = ZwaveAeotecSwitch6(firefly, package, **kwargs)
  return firefly.install_component(switch)

class ZwaveAeotecSwitch6(ZwaveSwitch):
  def __init__(self, firefly, package, **kwargs):
    initial_values = INITIAL_VALUES
    if kwargs.get('initial_values') is not None:
      initial_values_updated = INITIAL_VALUES.copy()
      initial_values_updated.update(kwargs.get('initial_values'))
      initial_values = initial_values_updated

    kwargs.update({
      'initial_values': initial_values,
      'commands':       COMMANDS,
      'requests':       REQUESTS
    })
    super().__init__(firefly, package, TITLE, capabilities=CAPABILITIES, **kwargs)

    self.set_alexa_categories(ALEXA_SMARTPLUG)

  def update_device_config(self, **kwargs):
    # TODO: Pull these out into config values
    # TODO Copy this retry logic to all zwave devices
    """
    Updated the devices to the desired config params. This will be useful to make new default devices configs.

    For example when there is a gen6 multisensor I want it to always report every 5 minutes and timeout to be 30
    seconds.
    Args:
      **kwargs ():
    """

    # Spec Sheet
    # TODO: Find spec sheet

    # TODO: Document These
    report = 2  # 1=hail 2=basic
    successful = self.verify_set_zwave_params([
      (110, 1),
      (100, 1),
      (80, report),
      (102, 15),
      (111, 30)
    ])
    self._update_try_count += 1
    self._config_updated = successful
