'''
holds many of the data structures needed by CCA1
these will be used by cca1.py module via instantiation ('g') in main_eval()
    of 'Multiple_sessions_data'  (also some global constants copied to g as well)
    include here variables which will persist between missions:
    performance_metric, event_log_memory
most other data variables are initiated at start of each mission (ie, each
    time main_mech.cycles() is called via instantiation ('d') of 'Mapdata'
'''
##START PRAGMAS
#
#temporary pylint bypasses during deprecation/transition devpt work
#pylint: disable=invalid-name
#   prefer not to use snake_case style for very frequent data structure or
#   for small temp variables
#pylint: disable=line-too-long
#pylint: disable=too-many-instance-attributes
#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#   use wildcard import for constants
##END PRAGMAS

from constants import *

class MultipleSessionsData:
    '''hold data here that should be kept between sessions as well
    as global constants
    '''
    def __init__(self):
        '''the following are initiated at program start via instant-
            iation of ddata.MultipleSessionsData -- 'g' instance:
        '''
        self.performance_metric: list = []
        self.event_log_memory = [['start of event_log_memory']]
        self.sensory_buffer: list = []
        self.debug = DEBUG
        self.fastrun = FASTRUN #True causes skipping of many user inputs
        self.autorun = AUTORUN #True will run whole session without user input
        self.mod_cycle_reevaluate = MOD_CYCLE_REEVALUATE
        self.version = VERSION
        self.hardware = HARDWARE
        self.display_system = DISPLAY_SYSTEM #nb verbose, print_references in code
        self.memory_checking_on_temp = MEMORY_CHECKING_ON_TEMP
        self.max_cycles = MAX_CYCLES
        self.total_rows = TOTAL_ROWS
        self.total_cols = TOTAL_COLS
        self.goal_random_walk = GOAL_RANDOM_WALK
        self.goal_skewed_walk = GOAL_SKEWED_WALK
        self.goal_precausal_find_hiker = GOAL_PRECAUSAL_FIND_HIKER
        self.goal_causal_find_hiker = GOAL_CAUSAL_FIND_HIKER
        self.tries_before_declare_local_minimum = TRIES_BEFORE_DECLARE_LOCAL_MINIMUM
        #self.default_vector = DEFAULT_VECTOR
        #self.default_goal = DEFAULT_GOAL
        #self.default_hippocampus = DEFAULT_HIPPOCAMPUS
        self.escape_left = ESCAPE_LEFT
        self.filler = FILLER
        self.reflex_escape = REFLEX_ESCAPE
        #self.initiate_value = INITIATE_VALUE


    def __str__(self)-> str:
        '''
        for developmental purposes
        values of the instance.MultipleSessionsData values
        '''
        print('\n*******dump: instance.MultipleSessionsData variables*****')
        print('self.performance_metric  ', self.performance_metric)
        print('self.event_log_memory  ', self.event_log_memory)
        print('self.sensory_buffer  ', self.sensory_buffer)
        print('self.debug  ', self.debug)
        print('self.fastrun  ', self.fastrun)
        print('self.autorun', self.autorun)
        print('self.mod_cycle_reevaluate  ', self.mod_cycle_reevaluate)
        print('self.version  ', self.version)
        print('self.display_system  ', self.display_system)
        print('self.memory_checking_on_temp  ', self.memory_checking_on_temp)
        print('for other variables change __str__ or parameters if possible')
        return '*******finished dump: instance.MultipleSessionsData variables*****\n'


    def qc(self, set_temp_true: bool = False, set_true: bool = False, set_false: bool = False)->None:
        '''quality control checkpoint
        if DEBUG is set then will run
        parameters:
            DEBUG is global which is initially put into self.debug
            set_temp_true - if flag then set_true set true only for
                            this qc call and then reverts back to previous value
            set_true - if flag this parameter then will set self.debug= True
            set_false - if flag this parameter then will set self.debug= False
        '''
        if set_true:
            self.debug = True
        if set_false:
            self.debug = False
        if self.debug or set_temp_true:
            print(self.__str__())


    def printout_event_log_memory(self)->bool:
        '''prints event_log memory and whatever analysis method provides
        '''
        print('\n', self.event_log_memory, '\n')
        return True


    def gevent_log(self, item: str, verbose: bool = False)->bool:
        '''goal and event_log module interacts with the emotional and reward module as well
         as the entire CCA1 to provide some overall control of the CCA1’s behavior
         memories of operations occurring in the logic/working memory are temporarily
          kept in the event_log module, allowing improved problem solving as well as
          providing more transparency to CCA1 decision making
        '''
        if verbose:
            print('CHECKPOINT: in event_log method')
        #nano ver emulate with simple list
        #add event_log item to event_log memory
        self.event_log_memory.append(item)
        print('in gevent_log')
        return True
