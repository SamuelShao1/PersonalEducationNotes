import re
from typing import Dict, Any, Tuple

def parse_tests(tests: str) -> None:
    """
    Parse the test cases from the provided file and execute them.
    
    :param tests: Path to the file containing test cases.
    """
    try:
        with open(tests, 'r') as file:
            data = file.read()
        test_dict = eval(re.search(r'TestDict\s*=\s*(\{.*\})', data, re.DOTALL).group(1))
        
        for case, info in test_dict.items():
            scenario = info['Scenario']
            use_case = info['UseCase']
            test_class = info['Class']
            test_data = info.get('testData', None)
            
            tx_use_case = parse_use_case(use_case, 'Tx')
            rx_use_case = parse_use_case(use_case, 'Rx')
            
            scenario_instance = Scenario(
                scenario=scenario,
                case=case,
                tx_use_case=tx_use_case,
                rx_use_case=rx_use_case,
                test_class=test_class,
                test_data=test_data
            )
            scenario_instance.run()
    except Exception as e:
        print(f"Failed to parse and run tests: {e}")

def parse_use_case(use_case: str, direction: str) -> Tuple[str, str, str]:
    """
    Parse the use case string to extract the use case details.
    
    :param use_case: The use case string.
    :param direction: The direction to parse ('Tx' or 'Rx').
    :return: A tuple with parsed use case details.
    """
    try:
        pattern = re.compile(rf'{direction}=(EN|DS)(-(600GB|1200GB|2400GB)|)')
        return pattern.search(use_case).groups()
    except AttributeError:
        print(f"Failed to parse {direction} use case from {use_case}")
        return ('DS', '', '0GB')

class Scenario:
    def __init__(self, scenario: str, case: str, tx_use_case: Tuple[str, str, str], 
                 rx_use_case: Tuple[str, str, str], test_class: str, test_data: Dict[str, Any]) -> None:
        self.scenario = scenario
        self.case = case
        self.tx_use_case = tx_use_case
        self.rx_use_case = rx_use_case
        self.test_class = test_class
        self.test_data = test_data
        self.is_tx_en = tx_use_case[0] == 'EN'
        self.is_rx_en = rx_use_case[0] == 'EN'
        self.tx_speed = tx_use_case[2] if self.is_tx_en else '0GB'
        self.rx_speed = rx_use_case[2] if self.is_rx_en else '0GB'
        self.tx_pin_list = ', '.join(self.pins(self.tx_speed)) if self.is_tx_en else []
        self.rx_pin_list = ', '.join(self.pins(self.rx_speed)) if self.is_rx_en else []

    def run(self) -> None:
        """
        Execute the scenario based on the type.
        """
        if self.scenario == "Get":
            self.get_eval()
        elif self.scenario == "Set":
            self.set()
        else:
            raise AttributeError("Unknown scenario.")

    def set(self) -> None:
        """
        ASSUMPTION: The only test case I saw 
        with Tx-DS-1200GB is Case5, but there seems to be an
        error with this test case as it later says 'tx-enable' : 'enabled'. Therefore,
        I assumed this was a type and meant to be Tx-EN. 
        ASSUMPTION: Then, for Tx-DS states I assumed instead of listing pins to just have an empty list.
        ASSUMPTION: Also unclear the critera if the entire config is enabled only if both RX and TX enabled (aka unclear about
        the case where TX xor RX is enabled. I assumed if the entire config is enabled based on if TX is enabled.
        """
        data = self.generate_set_data()
        self.summarize_set()
        print(f"Sending to device : {data}")

    def get_eval(self) -> None:
        """
        Evaluate the 'Get' scenario.
        """
        client_interface = self.test_data['client-interface']['data-path']
        ciena_line = self.test_data['ciena-line:dataPlane']

        #ASSUMPTION: Overall config enable is based on if TX is enabled.
        #NOTE: Code here could be modularized if we wanted more specific "FAIL" statements

        #TX Cases
        passed = self.is_tx_en and client_interface['config']['enabled'] #Client-interface Enabled field must be true
        passed &= ciena_line['config']['enable-laser'] #ciena-line enable-laser field must tbe true
        passed &= ciena_line['config']['laser-frequency'] > 0 #laser-frequency must be non zero
        
        cl_tx_config = ciena_line['tx']['config']
        passed &= cl_tx_config['tx-enable'] == 'enabled' #tx-enable must be true
        passed &= float(cl_tx_config['tx-power']) > 0 #tx-power must be non zero
        if not passed: 
            print("failed at tx_cases")

        #ASSUMPTION: Though not explicitly state, if rx is enabled then it should be displayed as such
        cl_rx_config = ciena_line['rx']['config']
        passed &= cl_rx_config['signal-class']['rx-enable'] == 'enabled' #rx-enable must be true

        try:
            #Speed cases
            passed &= client_interface['tx']['config']['speed-rating-mode'] == self.tx_speed # Speed ratings of the Client-interface must match
            passed &= self.tx_speed in ['0GB', '600GB', '1200GB', '2400GB'] #600GB, 1200Gb, and 2400GB are the only valid values unless it is DS (Disabled)
            tx_pin_list = client_interface['tx']['config']['serdes-pins-in-use']
            passed &= len(tx_pin_list) == int(self.tx_speed[:-2]) // 100 # Each Pin can do 100GB so a 600GB speed must have 6 pins a 1200GB speed must have 12 pins.
            for tx_pin in tx_pin_list:
                #ASSUMPTION, not sure how to deal with no pins when disabled as there wasn;t
                passed &= int(re.search(r'PIN_(\d+)', tx_pin).group(1)) < 32 #only available pins are 1-32
            passed &= len(tx_pin_list) == len(set(tx_pin_list)) # cannot be used more then once
        except KeyError:
            passed &= not self.is_tx_en #ASSUMPTION: check ci -> tx/rx doesnt exist when disabled 
        if not passed: 
            print("failed at tx_speed_cases")

        try:
            # Speed cases
            passed &= client_interface['rx']['config']['speed-rating-mode'] == self.rx_speed  # Speed ratings of the Client-interface must match
            passed &= self.rx_speed in ['0GB', '600GB', '1200GB', '2400GB']  # 600GB, 1200GB, and 2400GB are the only valid values unless it is DS (Disabled)
            rx_pin_list = client_interface['rx']['config']['serdes-pins-in-use']
            passed &= len(rx_pin_list) == int(self.rx_speed[:-2]) // 100  # Each Pin can do 100GB so a 600GB speed must have 6 pins a 1200GB speed must have 12 pins.
            for rx_pin in rx_pin_list:
                # ASSUMPTION, not sure how to deal with no pins when disabled as there wasn't
                passed &= int(re.search(r'PIN_(\d+)', rx_pin).group(1)) < 32  # Only available pins are 1-32
            passed &= len(rx_pin_list) == len(set(rx_pin_list))  # Cannot be used more than once
        except KeyError:
            passed &= not self.is_rx_en  # ASSUMPTION: check client-interface -> tx/rx doesn't exist when disabled
        if not passed: 
            print("failed at speed rx_cases")

        #validate_class(ciena_line['rx']['config']['signal-class'], test_class)
        #Class cases
        rx_signal_class = cl_rx_config['signal-class']
        if self.test_class == 'ModeA':
            #ASSUMPTION: 'signal-class-label should also match
            passed &= rx_signal_class['signal-class-label'] == self.test_class
            passed &= rx_signal_class['transport-mode'] == 'streaming'
            passed &= cl_tx_config['tfet-mode'] == 'off'
        elif self.test_class == 'ModeB':
            #ASSUMPTION: 'signal-class-label should also match
            passed &= rx_signal_class['signal-class-label'] == self.test_class
            passed &= rx_signal_class['transport-mode'] == 'off'
            passed &= cl_tx_config['tfet-mode'] == 'on'
        elif self.test_class == 'ModeC':
            #ASSUMPTION: 'signal-class-label should also match
            passed &= rx_signal_class['signal-class-label'] == self.test_class
            passed &= rx_signal_class['transport-mode'] == 'streaming'
            passed &= cl_tx_config['tfet-mode'] == 'on'
        
        self.summarize_get(result="PASS" if passed else "FAIL")

    def generate_set_data(self) -> Dict[str, Any]:
        """
        Generate the data for the 'Set' scenario.
        
        :return: A dictionary with the configuration data.
        """
        return {
            'client-interface': {
                'data-path': {
                    'config': {'enabled': self.is_tx_en},
                    'tx': {'config': {'speed-rating-mode': self.tx_speed, 'serdes-pins-in-use': self.tx_pin_list}},
                    'rx': {'config': {'speed-rating-mode': self.rx_speed, 'serdes-pins-in-use': self.rx_pin_list}}
                }
            },
            'ciena-line:dataPlane': {
                'config': {'laser-frequency': 5000 if self.is_tx_en else 0, 'enable-laser': self.is_tx_en},
                'rx': {
                    'config': {
                        'signal-class': {
                            'signal-class-label': self.test_class,
                            'transport-mode': 'off' if self.test_class == 'ModeB' else 'streaming',
                            'rx-enable': self.is_rx_en
                        }
                    }
                },
                'tx': {
                    'config': {
                        'tx-enable': 'enabled' if self.is_tx_en else 'disabled',
                        'tx-power': '44.000' if self.is_tx_en else "0",
                        'tfet-mode': 'off' if self.test_class == 'ModeA' else 'on'
                    }
                }
            }
        }

    def summarize_set(self) -> None:
        """
        ASSUMPTIONS: Some formatting decisions as only a both tx-en and rx-en example was show.
                     Listed out pins in a more readable way. 
        """
        print(f"""
            Case Number: {re.search(r'\d+', str(self.case)).group()}
            Scenario: {self.scenario.upper()}
            TX Case: Setting Speed to {self.tx_speed} and Pins to {(self.tx_pin_list) if self.is_tx_en else "None"}
            RX Case: Setting Speed to {self.rx_speed} and Pins to {(self.rx_pin_list) if self.is_rx_en else "None"}
            Class: Set mode to {self.test_class.replace("Mode", "Mode ")}
            Client-Interface: Enabling Interface
            Client-Interface TX: Setting Speed to {self.tx_speed} and Pins to {(self.tx_pin_list) if self.is_tx_en else "None"}
            Client-Interface RX: Setting Speed to {self.rx_speed} and Pins to {(self.rx_pin_list) if self.is_rx_en else "None"}
            Ciena-Line: Setting Laser Frequency to {self.is_tx_en}
            Ciena-Line Tx: Turning {'on' if self.is_tx_en else 'off'} Tx-Enable and setting Tx Power to {'non zero' if self.is_tx_en else 'zero'}
            Ciena-Line Rx: {'Enabling' if self.is_rx_en else 'Disabling'} Rx Enable
            Ciena-Line Signal Class: Setting Signal Class to {self.test_class}
        """)

    def summarize_get(self, result: str = '') -> None:
        """
        ASSUMPTIONS: Some formatting decisions as only a both tx-en and rx-en example was shown.
                    Listed out pins in a more readable way. 
        """
        try:
            tx_pins_count = len(self.test_data['client-interface']['data-path']['tx']['config']['serdes-pins-in-use'])
            tx_line = f"Client-Interface Tx: {result} Speed is {self.tx_speed} and Pin count is {tx_pins_count}"
        except KeyError:
            tx_line = f"Client-Interface Tx: {result} Speed is {self.tx_speed} and Pin count is 0"
        try:
            rx_pins_count = len(self.test_data['client-interface']['data-path']['rx']['config']['serdes-pins-in-use'])
            rx_line = f"Client-Interface Rx: {result} Speed is {self.rx_speed} and Pin count is {rx_pins_count}"
        except KeyError:
            rx_line = f"Client-Interface Rx: {result} Speed is {self.rx_speed} and Pin count is 0"

        case_number = re.search(r'\d+', str(self.case)).group()
        scenario_upper = self.scenario.upper()
        formatted_test_class = self.test_class.replace("Mode", "Mode ")

        laser_freq_set = 'set' if self.test_data['ciena-line:dataPlane']['config']['laser-frequency'] > 0 else 'not set'
        laser_enabled = 'enabled' if self.test_data['ciena-line:dataPlane']['config']['enable-laser'] else 'disabled'
        laser_connector = "and" if laser_freq_set == 'set' and laser_enabled == 'enabled' else "but"

        tx_enabled = 'set' if self.test_data['ciena-line:dataPlane']['tx']['config']['tx-enable'] == 'enabled' else 'not set'
        tx_power_non_zero = 'non-zero' if float(self.test_data['ciena-line:dataPlane']['tx']['config']['tx-power']) > 0 else 'zero'
        tx_connector = "and" if tx_enabled == 'set' and tx_power_non_zero == 'non-zero' else "but"
        
        rx_enabled = 'set' if self.test_data['ciena-line:dataPlane']['rx']['config']['signal-class']['rx-enable'] == 'enabled' else 'not set'

        print(f"""
            Case Number = {case_number}
            SCENARIO = {scenario_upper}
            TX Case = {self.tx_speed} {'Enabled' if self.is_tx_en else 'Disabled'}
            RX Case = {self.rx_speed} {'Enabled' if self.is_rx_en else 'Disabled'}
            Class = {formatted_test_class}
            Client-Interface: {result} Enabled = {self.is_tx_en}
            {tx_line}
            {rx_line}
            Ciena-Line: {result} Laser Frequency is {laser_freq_set} {laser_connector} enable-laser is {laser_enabled}
            Ciena-Line Tx: {result} Tx Enable is {tx_enabled} {tx_connector} tx-power is {tx_power_non_zero}
            Ciena-Line Rx: {result} Rx Enable is {rx_enabled}
            Ciena-Line Signal Class: {result} Mode is set correct to {formatted_test_class}
        """)

    def pins(self, speed: str):
        return ['PIN_{}'.format(i) for i in range(int(speed[:-2]) // 100)]

def main():
    tests = "Dicts.txt"
    parse_tests(tests)

if __name__ == "__main__":
    main()
