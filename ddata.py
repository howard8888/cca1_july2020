'''
holds many of the data structures needed by CCA1
these will be used by cca1.py module via instantiation ('g') in main_eval()
    of 'Multiple_sessions_data'  (also some global constants copied to g as well)
    include here variables which will persist between missions:
    performance_metric, conscious_memory
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
#pylint: disable=dangerous-default-value
#pylint: disable=too-many-public-methods
#   a number of methods in class MapData are being deprecated and
#   switched to Class NavMod
##END PRAGMAS

import copy
from constants import *


class MapData:
    '''most of the data variables are held here in Mapdata class
    '''
    def __init__(self):
        '''these data variables are initiated at start of each mission (ie,
                each time main_mech.cycles is called) -- 'd' instance
           be aware the following are initiated at program start via instant-
                iation of ddata.MultipleSessionsData -- 'g' instance:
                    performance_metric: list = []
                    conscious_memory = [['start of conscious_memory']]
                    sensory_buffer: list = []
        '''
        self.debug = DEBUG
        self.meaningfulness = False
        self.performance_metric_per_mission = INITIATE_VALUE
        self.evaluation_cycles = INITIATE_VALUE
        self.age_autonomic_calls = INITIATE_VALUE
        self.current_autonomic = FILLER
        self.current_instinct = FILLER
        self.current_goal = DEFAULT_GOAL
        self.current_hippocampus = DEFAULT_HIPPOCAMPUS
        self.h_mem_dirn_goal = None
        self.h_mem_prev_dirn_goal = None
        self.local_minimum = INITIATE_VALUE
        #as detailed below positions are matrix (m,n) coordinates
        self.cca1_position = [INITIATE_VALUE, INITIATE_VALUE]
        self.hiker_position = [INITIATE_VALUE, INITIATE_VALUE]
        self.visual_obstruction = '11111100'
        self.auditory_obstruction = '00000000'

        #forest_map is map observer can see, but cca1 agent does not have this knowledge
        #int_map is the internal map of cca1 agent, ie, its knowledge of the envrt
        #using matrix (m,n) coordinate, NOT (x,y) coordinates
        #thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        #thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        self.forest_map = [['edge', 'edge', 'edge', 'edge', 'edge', 'edge'],
                           ['edge', 'forest', 'forest', 'sh_rvr', 'forest', 'edge'],
                           ['edge', 'lake  ', 'forest', 'forest', 'forest', 'edge'],
                           ['edge', 'forest', 'wtrfall', 'forest', 'forest', 'edge'],
                           ['edge', 'forest', 'forest', 'forest', 'forest', 'edge'],
                           ['edge', 'edge', 'edge', 'edge', 'edge', 'edge']]
        self.int_map = [['edge', '', '', '', '', 'edge'],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['edge', '', '', '', '', 'edge']]

        #CCA1 architecture has adopted a map as the basic data object for all cognition
        #in keeping with the CCA1 paper terminology, nav_map represents the Navigation Module 'temporary map',
        #ie, the current map the Navigation Module is operating on
        #c_maps represent the store of 'temporary maps' the Navigation Module stores in the Causal Memory Module
        self.nav_map = [[['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']],
                        [['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']],
                        [['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']],
                        [['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']],
                        [['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']],
                        [['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null'], ['', 'null', 'null', 'null']]]
        self.c_map = [['empty 0th element']]
        self.l_map = []
        self.c_stack = []
        self.c_stack1 = []
        self.c_stack2 = []
        self.memory_description_string = '''
        Causal Memory Stacks ('c_stackx' list variables):
        Note: Even though we are treating as such for programmatic ease, these
        collections of 'temporary navigation maps' should be thought of more as
        a searchable non-ordered collections of temporary maps than as computer stacks.
        Temporary maps stored in the Causal Memory Module (c_map list) or
         integrated into the Learned Primitives or other portions of the CCA1
         should be considered as similar to 'Long Term Memory'.
        The current 'temporary map' should be considered as similar to 'Working
          Memory', ie, information is actively manipulated on it.")
        The 'c_stacks' should be considered a 'Short Term Memory' that can be or
          are not moved back to the current 'temporary map' and/or stored into
          the 'Long Term Memory' (c_map list and other parts of the architecture))
        Note that the 'Long Term Memory' (c_map list) as well as the 'Short Term Memory'
          (c_stacks) are organized in terms of maps, more so the Long Term Memory, and
          the 'Short Term Memory' (c_stacks) as it persists for a while in activity.)
        l_map (for 'long term causal memory map) is created from c_map at present, but
          as code development proceeds c_map will be deprecated and l_map will be 
          created directly -- l_map is not a list of maps but a hierarchy of maps 
          all organized in the 6x6 format of nav_map and branching out
        '''

        #this emulation/simulation pretends that the 'sensory_inputs' lists below are
        #values received from a video camera/pre-processor, audio/pre-processor, etc
        #visual_inputs data structure is as follows:
        # [ [ possible vector inputs for square 0,0 i,e square 0],
        #    ....
        #  [ possible vector inputs for square 3,3 i,e square 15]  ]
        #data structure of possible vector inputs for any square, eg,#0, is:
        #  [ [possible values for North visual input],[possibles for E],[S],[W] ]
        #thus if the CCA1 is in square 0 right now, then possible values for its
        #video camera/pre-processor to pretend to receive from the North are:
        #['11111100', '11111101', '11011000', '10011100'] -- the software routines
        #will randomly select one of these values, eg, perhaps '11111101'
        #thus in this example when the CCA1 is in square 0 its camera reports
        #visual input '11111101' from the North
        #programmatically this is represented as visual_inputs[0][0][1]
        #(note that these visual inputs, the 8 bits of video input,
        #are an emulation of what a video camera would produce if it was looking
        #at the squares around (ie, N,E,S,W -- 4 values) and looking at that moment
        #North of square 0, given the landscape features in forest_map (ie, these
        #values are a real emulation/simulation of what a video camera would be
        #reporting for that landscape of the gridworld being used, plus of course
        #some noise and randomness at what the camera is looking at emulated by the
        #different but close possible choices for each direction)
        self.visual_inputs = [[['191111100', '119111101', '119011000', '100911100'], ['110800110', '110080111', '110180110', '110800010'], ['110000711', '111107111', '100171111', '011711111'], ['111116100', '161111101', '110161000', '100161100']],
                              [['11111100', '11111101', '11011000', '10011100'], ['00010001', '00010011', '10010001', '00010101'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['00010001', '00010011', '10010001', '00010101']],
                              [['11100110', '11100111', '11110110', '11100010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000011', '11110111', '10011111', '01111111']],
                              [['00010001', '00010011', '10010001', '00010101'], ['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000011', '11110111', '10011111', '01111111'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011'], ['01010000', '01110000', '01010001'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011']],
                              [['11000110', '11000111', '11010110', '11000010'], ['01010000', '01110000', '01010001'], ['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010']],
                              [['00011001', '00011011'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['01010000', '01110000', '01010001']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010']]]
        #trying to make all data objects more uniform in the form of the 6x6x*x matrix we are using
        #EDGE_MODE == True: '??' -- CCA1 agent should not be in that square getting an 'invalid' == '??' sensory input since that is an edge square  and cannot move there
        #EDGE_MODE == False: '??' --> edge and position codes -- in this mode allow 6x6 to be used without edge cells
        self.visual_database = [[[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.visual_inputs[0], self.visual_inputs[1], self.visual_inputs[2], self.visual_inputs[3], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.visual_inputs[4], self.visual_inputs[5], self.visual_inputs[6], self.visual_inputs[7], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.visual_inputs[8], self.visual_inputs[9], self.visual_inputs[10], self.visual_inputs[11], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.visual_inputs[12], self.visual_inputs[13], self.visual_inputs[14], self.visual_inputs[15], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]]]
        #auditory_inputs same data structure as visual_inputs
        self.auditory_inputs = [[['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000'], ['00000000', '00000010', '00000001', '00100000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000']],
                                [['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011'], ['11110000', '11110001', '11110010', '11110100'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11110000', '11110001', '11110010', '11110100'], ['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000']],
                                [['01010101', '01010111', '01010011', '01000011'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11110000', '11110001', '11110010', '11110100']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000']]]
        #trying to make all data objects more uniform in the form of the 6x6x*x matrix we are using
        #EDGE_MODE == True: '??' -- CCA1 agent should not be in that square getting an 'invalid' == '??' sensory input since that is an edge square  and cannot move there
        #EDGE_MODE == False: '??' --> edge and position codes -- in this mode allow 6x6 to be used without edge cells
        self.auditory_database = [[[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                  [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.auditory_inputs[0], self.auditory_inputs[1], self.auditory_inputs[2], self.auditory_inputs[3], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                  [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.auditory_inputs[4], self.auditory_inputs[5], self.auditory_inputs[6], self.auditory_inputs[7], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                  [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.auditory_inputs[8], self.auditory_inputs[9], self.auditory_inputs[10], self.auditory_inputs[11], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                  [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], self.auditory_inputs[12], self.auditory_inputs[13], self.auditory_inputs[14], self.auditory_inputs[15], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]],
                                  [[['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']], [['??', '??', '??', '??'], ['??', '??', '??', '??'], ['??', '??', '??', '??']]]]
        #
        self.visual_dict = {'11100011':'lake', '01010000':'lost hiker visual', '11111100':'obstruction', '00010001':'shallow river', '00011001':'shallow river + spraying water',
                            '11000110':'forest'}
        self.auditory_dict = {'00000000':'strange silence', '11000000':'forest_noise', '11110000':'human cry help', '00010001':'smooth water sound', '11100000':'bird mating call', '01010101':'water spray noise'}
        self.fused_dict = {'1110001100010001':'lake + smooth water sound -> lake', '1100011011000000':'forest + forest noise -> forest',
                           '0001000100010001':'shallow river + smooth water sound -> shallow_river', '0001100101010101':'shallow river + spraying water + water spray noise -> waterfall',
                           '0101000011110000':'lost hiker visual + human cry help -> hiker', '1111110000000000':'obstruction + strange silence -> edge',
                           '1001111110011111':'forest value used for causal demo case -> forest'}
        #instinct values are goal action values to shape output
        self.instinct_dict = {'10000000':'forward eat/goal', '11000000':'left avoid', '01000000':'right avoid', '00000000':'conserve energy'}
        #autonomic values will shape instinct value along with sensory input values
        self.autonomic_dict = {'00000000':'conserve energy', '00000001':'move to different area',
                               '00000010':'eat', '00000011':'reproduce'}
        #intuit_instinct values are procedural vectors triggered in intuitive logic/physics/psychology or goal plannig
        self.intuitive_instinct_dict = {'1111110000000000':'edge_logic',
                                        '1110001100010001':'water_everywhere_logic',
                                        '0001100101010101':'water_everywhere_logic'}
        #learned_instinct values are procedural vectors triggered in learned logic/physics/psychology or goal plannig
        self.learned_instinct_dict = {'0001000100010001':'test_case_learned'}
        #


    def __str__(self)-> str:
        '''
        for developmental purposes
        values of the instance.MapData values
        '''
        print('\n*******dump: instance.MapData variables*****')
        print('self.meaningfulness ', self.meaningfulness)
        print('self.performance_metric_per_mission', self.performance_metric_per_mission)
        print('self.evaluation_cycles', self.evaluation_cycles)
        print('self.age_autonomic_calls', self.age_autonomic_calls)
        print('self.current_autonomic', self.current_autonomic)
        print('self.current_instinct', self.current_instinct)
        print('self.current_goal', self.current_goal)
        print('self.current_hippocampus', self.current_hippocampus)
        print('self.h_mem_dirn_goal', self.h_mem_dirn_goal)
        print('self.h_mem_prev_dirn_goal', self.h_mem_prev_dirn_goal)
        print('self.local_minimum', self.local_minimum)
        print('self.cca1_position', self.cca1_position)
        print('self.hiker_position', self.hiker_position)
        print('\nself.forest_map', self.forest_map)
        print('\nself.int_map', self.int_map)
        self.print_forest_map()
        print('for other variables change __str__ or parameters if possible')
        #print('\nself.visual_inputs', self.visual_inputs)
        #print('\nself.auditory_inputs', self.auditory_inputs)
        #print('\nself.visual_dict', self.visual_dict)
        #print('self.auditory_dict', self.auditory_dict)
        #print('self.fused_dict', self.fused_dict)
        #print('self.instinct', self.instinct_dict)
        #print('self.autonomic', self.autonomic_dict)
        #print('self.intuitive_instinct', self.intuitive_instinct_dict)
        #print('self.learned_instinct', self.learned_instinct_dict)
        return '*******finished dump: instance.MapData variables*****\n'


    def gpu_resources_initialize(self)-> bool:
        '''initialize resources for holding and processing data
        at present local python envr't is used
        '''
        if self.debug:
            print('Session resources have been successfully set up')
        return True


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


    def print_int_map(self, print_nav_map_also: bool=True)-> bool:
        '''prints out CCA1's internal map of the forest which CCA1 has constructed
        from its explorations
        #forest_map is map observer can see, but cca1 agent does not have this knowledge
        #int_map is the internal map of cca1 agent, ie, its knowledge of the envrt
        #using matrix (m,n) coordinate, NOT (x,y) coordinates
        #thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        #thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        -int_map is slowly being deprecated and replaced by nav_map in ongoing code updates
        -note that parameters all set to True at time of writing, thus when call
            print_int_map() then this also calls int_map_to_nav_map() which
            also calls print_nav_map()[0] elements which also calls nav_map_to_c_map,
            which causes 'temporary nav_maps' to be stored in causal memory c_map
        -set print_nav_map_also=False if don't want to cause nav_map updating and printing
        '''
        if print_nav_map_also:
            self.int_map_to_nav_map(True)
        return_value = True
        if self.current_goal in (GOAL_SKEWED_WALK, GOAL_RANDOM_WALK):
            print('curent goal is: ', self.current_goal)
            print('CCA1 is functioning via random/skewed walk and no internal maps constructed\n')
            print('current values for the CCA1s internal map are as follows: ')
            return_value = False
        horizontals = "---------------------------------------------------------------------------------------"
        print("\nCCA1's own internal map of the Forest (* is position of CCA1 {})".format(self.cca1_position))
        print("nb. This is internal map *before* move is made by CCA1")
        print(horizontals + '-')
        m = -1
        for i in self.int_map:
            m = m + 1
            n = -1
            for j in i:
                n = n + 1
                if self.cca1_position == (m, n):
                    j = j + '*'
                print(j.ljust(10), end='  |  ')
            print('\n', horizontals)
        return return_value

    def print_forest_map(self)-> bool:
        '''prints out bird's-eye view of forest from system values
        CCA1 does not have this information but must build up its own int_map
        #new structure for forest_map making it more similar to int_map
        #forest_map is map observer can see, but cca1 agent does not have this knowledge
        #int_map is the internal map of cca1 agent, ie, its knowledge of the envrt
        #using matrix (m,n) coordinate, NOT (x,y) coordinates
        #thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        #thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        '''
        horizontals = "---------------------------------------------------------------------------------------"
        print("\nBird's-Eye View of Forest (CCA1 does not have this view)")
        print(horizontals + '-')
        m = -1
        for i in self.forest_map:
            m = m + 1
            n = -1
            for j in i:
                n = n + 1
                if self.cca1_position == (m, n):
                    j = j + '*'
                print(j.ljust(10), end='  |  ')
            print('\n', horizontals)
        return True


    def set_hiker(self, m: int, n: int)-> tuple:
        '''sets hiker position on the forest map
        m rows x n columns coordinates, start 0,0 but edges thus corner position 1,1
        -forest_map is map observer can see, but cca1 agent does not have this knowledge
        -int_map is the internal map of cca1 agent, ie, its knowledge of the envrt
        -using matrix (m,n) coordinate, NOT (x,y) coordinates
        thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        -development note: keep hiker set to -yx(3, 1)=mn(3,1) for now until method's
        sensory assessments improved
        '''
        #check validity of inputs
        m = int(m)
        n = int(n)
        if m < 1:
            m = 1
            print('debug: m min coordinate error -- reset to 1')
        if n < 1:
            n = 1
            print('debug: n min coordinate error -- reset to 1')
        if m >= len(self.forest_map[0]) - 1:
            m = len(self.forest_map[0]) - 2
            print('debug: m max coordinate error -- reset to ', m)
        if n >= len(self.forest_map[0]) - 1:
            n = len(self.forest_map[0]) - 2
            print('debug: n max coordinate error -- reset to ', n)
        #set hiker position in forest_map
        #we do not set in int_map since int_map built up by agent
        self.hiker_position = (m, n)
        if self.forest_map[m][n] == 'CCA1  ':
            self.forest_map[m][n] = 'RESCUE'
            #if set hiker position onto CCA1 position then hiker is
            #automatically rescued
            print('\n**hiker placed in square where CCA1 already is')
            print('CCA1 has thus rescued lost hiker**')
        elif self.forest_map[m][n] == 'RESCUE':
            print('\n**hiker placed in RESCUE square')
            print('thus CCA1 has already rescued lost hiker**')
            #TBD if need
        else:
            #otherwise change forest_map square label
            self.forest_map[m][n] = 'hiker '
            print('\nhiker position set to: ', m, n)
        self.print_forest_map()
        return m, n


    def set_cca1(self, m: int, n: int)-> tuple:
        '''sets CCA1 position on the forest map
        m rows x n columns coordinates, start 0,0 but edges thus corner position 1,1
        -forest_map is map observer can see, but cca1 agent does not have this knowledge
        -int_map is the internal map of cca1 agent, ie, its knowledge of the envrt
        -using matrix (m,n) coordinate, NOT (x,y) coordinates
        thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        -if forest_map[x][y] == 'hiker ' -> forest_map[x][y] = 'RESCUE'
        -if forest_map[x][y] == 'RESCUE' -> print....
        -else forest_map[x][y] = 'CCA1  ' &  cca1_position = x, y
        -print_forest() and return (m,n)
        '''
        #check validity of inputs
        m = int(m)
        n = int(n)
        if m < 1:
            m = 1
            print('debug: m min coordinate error -- reset to 1')
        if n < 1:
            n = 1
            print('debug: n min coordinate error -- reset to 1')
        if m >= len(self.forest_map[0]) - 1:
            m = len(self.forest_map[0]) - 2
            print('debug: m max coordinate error -- reset to ', m)
        if n >= len(self.forest_map[0]) - 1:
            n = len(self.forest_map[0]) - 2
            print('debug: n max coordinate error -- reset to ', n)
        #set cca1 position in forest_map
        #we do not set in int_map since int_map built up by agent
        #however, cca1 agent does know what its current location is, ie,
        #it does have access to cca1_position, but not forest_map
        if self.forest_map[m][n] == 'hiker ':
            #if cca1 lands on hiker then hiker is considered rescured
            self.forest_map[m][n] = 'RESCUE'
            #hiker square will now display 'RESCUE' rather than 'HIKER'
            self.cca1_position = m, n
            #actually set the cca1_position now
            print('\n**CCA1 has rescued lost hiker**')
        elif self.forest_map[m][n] == 'RESCUE':
            #if continue the mission despite rescue this can be called
            print('\n**CCA1 has rescued lost hiker**')
        else:
            #otherwise set cca1_position and change forest_map square label
            self.cca1_position = m, n
            self.forest_map[m][n] = 'CCA1  '
            print('\nCCA1 position set to: ', m, n)
        self.print_forest_map()
        return m, n


    def int_map_to_nav_map(self, print_map:bool=True)-> bool:
        '''copies the int_map to the nav_map
        as the modules of the July 2020 rewrite evolve from hard-wired blocks to more
        functional units following the CCA1 specifications, int_map will gradually
        be replaced by the nav_map, until eventually int_map will no longer be used
        -if print_map is True then also prints out a neat copy, ie, just element [0]
        '''
        for i in range(TOTAL_ROWS):
            for j in range(TOTAL_COLS):
                self.nav_map[i][j][0] = self.int_map[i][j]
        print('\nint_map copied to nav_map')
        if print_map:
            self.print_nav_map()
        return True


    def nav_map_to_int_map(self, print_map:bool=True)-> bool:
        '''copies the nav_map to the int_map
        as the modules of the July 2020 rewrite evolve from hard-wired blocks to more
        functional units following the CCA1 specifications, int_map will gradually
        be replaced by the nav_map, until eventually int_map will no longer be used
        -if print_map is True then also prints out a neat copy, ie, just element [0]
        '''
        for i in range(TOTAL_ROWS):
            for j in range(TOTAL_COLS):
                self.int_map[i][j] = self.nav_map[i][j][0]
        print('\nnav_map copied to int_map')
        if print_map:
            self.print_int_map(False)
        return True


    def print_nav_map(self, accumulate_map_into_c_map: bool=True, show_all_values: bool=True)-> bool:
        '''prints out CCA1's nav_map, which corresponds to the 'Temporary Map' of the
        CCA1's Navigaton Module
        #using matrix (m,n) coordinate, NOT (x,y) coordinates
        #thus as move horizontally the columns increase, (m,n++) NOT (x++,y)
        #thus as move vertically down the rows increase (m++,n)  NOT (x,y--)
        -if accumulate_map_into_c_map == True, then appends the current nav_map
            into c_map, ie, as per the CCA1 architecture it stores another 'tempoary map'
            into the Causal Memory Module
        -if show_all_values == True then prints out not only what is in each square of the map,
            but also where each square links to
        '''
        horizontals = "---------------------------------------------------------------------------------------"
        print("\nCCA1 'Temporary Map' ('nav_map')")
        print(horizontals + '-')
        for i in range(TOTAL_ROWS):
            for j in range(TOTAL_COLS):
                if show_all_values:
                    print(self.nav_map[i][j], end='  |  ')
                else:
                    print(self.nav_map[i][j][0].ljust(10), end='  |  ')
            print('\n', horizontals)
        if accumulate_map_into_c_map:
            self.nav_map_to_c_map()
        return True


    def nav_map_to_c_map(self)-> bool:
        '''appends the current nav_map into c_map, ie, as per the CCA1 architecture
            it stores another 'tempoary map' into the Causal Memory Module
        '''
        self.c_map.append(self.nav_map)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('CCA1 Causal Memory Module\n')
        print('To be deprecated to map-based insert version.')
        return True


    def print_c_map(self)-> bool:
        '''prints out c_map, ie, as per the CCA1 architecture
           the Causal Memory Module
        '''
        print('\nThe contents of the Causal Memory Module (c_map) are:')
        if self.c_map == []:
            print('The Causal Memory Module c_map has no saved maps at present\n')
            return False
        for i in self.c_map:
            for j in i:
                print(j)
        print()
        print('\n\n')
        return True


    def nav_map_to_c_stack(self)-> bool:
        '''appends the current nav_map onto the c_stack, ie, short-term memory
        '''
        self.c_stack.append(self.nav_map)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('c_stack short-term memory.\n')
        print('To be deprecated to map-based insert version.')
        return True


    def nav_map_to_c_stack1(self)-> bool:
        '''appends the current nav_map onto the c_stack, ie, short-term memory
        '''
        self.c_stack1.append(self.nav_map)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('c_stack1 short-term memory.\n')
        print('To be deprecated to map-based insert version.')
        return True


    def nav_map_to_c_stack2(self)-> bool:
        '''appends the current nav_map onto the c_stack, ie, short-term memory
        '''
        self.c_stack2.append(self.nav_map)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('c_stack2 short-term memory.\n')
        print('To be deprecated to map-based insert version.')
        return True


    def clear_c_stacks(self, stack: bool=True, stack1: bool=True,stack2: bool=True)-> bool:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        clear temporary map stacks
        '''
        if stack:
            self.c_stack = []
            print('c_stack cleared')
        if stack1:
            self.c_stack1 = []
            print('c_stack1 cleared')
        if stack2:
            self.c_stack2 = []
            print('c_stack1 cleared')
        return True


    def print_c_stacks(self, stack: bool=True, stack1: bool=True,stack2: bool=True)-> bool:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        print temporary map stacks
        '''
        #print(self.memory_description_string)
        if stack:
            for i in self.c_stack:
                for j in i:
                    print(j)
            print('**** --------> above was c_stack ****')
        if stack1:
            for i in self.c_stack1:
                for j in i:
                    print(j)
            print('**** --------> above was c_stack1 ****')
        if stack2:
            for i in self.c_stack2:
                for j in i:
                    print(j)
            print('**** --------> above was c_stack2 ****')
        return True


    def c_stack_to_c_map(self)-> int:
        '''appends c_stack into c_map, ie, as per the CCA1 architecture
            it stores another 'tempoary map' into the Causal Memory Module
        '''
        self.c_map.append(self.c_stack)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('CCA1 Causal Memory Module ie c_map\n')
        print('To be deprecated to map-based insert version.')
        return True


    def c_stack1_to_c_map(self)-> int:
        '''appends c_stack into c_map, ie, as per the CCA1 architecture
            it stores another 'tempoary map' into the Causal Memory Module
        '''
        self.c_map.append(self.c_stack1)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('CCA1 Causal Memory Module, ie c_map\n')
        print('To be deprecated to map-based insert version.')
        return True


    def c_stack2_to_c_map(self)-> int:
        '''appends c_stack2 into c_map, ie, as per the CCA1 architecture
            it stores another 'tempoary map' into the Causal Memory Module
        '''
        self.c_map.append(self.c_stack2)
        print('Current temporary map, ie, nav_map, has been appended to the')
        print('CCA1 Causal Memory Module,ie c_map\n')
        print('To be deprecated to map-based insert version.')
        return True


    def trigger_c_map(self, engram_trigger: list, engram_is_map_segment: bool=False)-> list:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        the Causal Memory Module returns the closest stored 'temporary map' (using the CCA1s
            nomenclature, realizing that these maps actually become permanent) to the input which
            is the list of values in engram_trigger
        if the engram_is_map_segment == True, then the search is looking for the most similar map,
            rather than the contents of the engram_trigger themselves
        returns a temporary memory and puts this temporary memory into the Navigation Module while
            automatically putting the current temporary memory in the Navigation Module onto the
            the short-term memory stack
        '''
        print(self.c_map, engram_trigger, engram_is_map_segment) #avoid triggering pylint
        return [-1]


    def trigger_c_stack(self, engram_trigger: list, engram_is_map_segment: bool=False)-> list:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        c_stack returns the closest stored 'temporary map' (using the CCA1s
            nomenclature, realizing that these maps actually become permanent) to the input which
            is the list of values in engram_trigger
        if the engram_is_map_segment == True, then the search is looking for the most similar map,
            rather than the contents of the engram_trigger themselves
        returns a temporary memory and puts this temporary memory into the Navigation Module while
            automatically putting the current temporary memory in the Navigation Module onto the
            the short-term memory stack
        '''
        print(self.c_map, engram_trigger, engram_is_map_segment) #avoid triggering pylint
        return [-1]


    def trigger_c_stack1(self, engram_trigger: list, engram_is_map_segment: bool=False)-> list:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        c_stack returns the closest stored 'temporary map' (using the CCA1s
            nomenclature, realizing that these maps actually become permanent) to the input which
            is the list of values in engram_trigger
        if the engram_is_map_segment == True, then the search is looking for the most similar map,
            rather than the contents of the engram_trigger themselves
        returns a temporary memory and puts this temporary memory into the Navigation Module while
            automatically putting the current temporary memory in the Navigation Module onto the
            the short-term memory stack
        '''
        print(self.c_map, engram_trigger, engram_is_map_segment) #avoid triggering pylint
        return [-1]


    def trigger_c_stack2(self, engram_trigger: list, engram_is_map_segment: bool=False)-> list:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        c_stack returns the closest stored 'temporary map' (using the CCA1s
            nomenclature, realizing that these maps actually become permanent) to the input which
            is the list of values in engram_trigger
        if the engram_is_map_segment == True, then the search is looking for the most similar map,
            rather than the contents of the engram_trigger themselves
        returns a temporary memory and puts this temporary memory into the Navigation Module while
            automatically putting the current temporary memory in the Navigation Module onto the
            the short-term memory stack
        '''
        print(self.c_map, engram_trigger, engram_is_map_segment) #avoid triggering pylint
        return [-1]


    def parse_nav_map_to_objects(self, object_sensitivity: int =50)-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and identifies objects in the map that have not been identified yet,
        and attempts to label these objects.
        -object_sensitivity adjusts how readily it parses out objects, varies 0 - 100
        -writes back directly to nav_map
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100,
        '''
        print(self.nav_map, object_sensitivity) #avoid triggering pylint
        return 50


    def parse_nav_map_to_agents(self, agent_sensitivity: int =50, require_movement: bool=False)-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and c_stack, c_stack1, cstack2,  and identifies agents in these maps
          that have not been identified yet, and attempts to label these agent.
        -agent_sensitivity adjusts how readily it parses out agents, varies 0 - 100
        -require_movement if True will require movement for labelling as agent
        -writes back directly to nav_map
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100
        '''
        print(self.nav_map, agent_sensitivity, require_movement) #avoid triggering pylint
        return 50


    def parse_nav_map_to_numbers(self, counting_sensitivity: int =50)-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and counts number of objects/agents in these maps
          and attempts to label each of these objects/agents with total and similar number
        -agent_sensitivity adjusts how readily it counts an object/agent, varies 0 - 100
        -writes back directly to nav_map
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100
        '''
        print(self.nav_map, counting_sensitivity) #avoid triggering pylint
        return 50


    def parse_nav_map_to_magnitude(self, size_sensitivity: int =50)-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and computes magnitude of size/effect of objects/agents in these maps
          and attempts to label each of these objects/agents with a magnitude number
        -agent_sensitivity adjusts how readily it sizes an object/agent, varies 0 - 100
        -writes back directly to nav_map
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100
        '''
        print(self.nav_map, size_sensitivity) #avoid triggering pylint
        return 50


    def parse_nav_map_to_transitivity_map(self, transitive_objects: list=['agents'], transitivity_sensitivity: int =50)-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and creates a transitivity map, ie, topological/schematic-like map, similar to
          a subway map, showing more clearly what items of interest are next to other items of interest
        -writes directly to c_stack2
        -calculates distances between nodes on the transitivity map and labels the nodes with these distances
        -transitive_objects are optional objects or agents the method should pay attention while creating
          a transitivity map
        -transitivity_sensitivity adjusts how readily it includes an object/agent, varies 0 - 100
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100
        '''
        print(self.nav_map, transitive_objects, transitivity_sensitivity) #avoid triggering pylint
        return 50


    def navigate_nav_map(self, starting_point: str='start', goal: str='wander')-> int:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        Takes nav_map and navigates towards goal point
        -will automatically output one navigation signal, and then a processing cycle has to occur again to
            call this method again and output the next navigational signal
        -if next location is off the current nav_map then it will put the current nav_map onto the c_stack,
            and attempt the contiguous required temporary map from one of the c_stack's or c_map, and this map
            then becomes the current nav_map
        -usually creates a transitivity map, ie, topological/schematic-like map, similar to
          a subway map, showing more clearly what items of interest are next to other items of interest, placing
          nav_map onto a c_stack and using the transitivity map as the current nav_map
        -the starting point can be specified and will be best matched on the nav_map or another map retrieved from c_map
        -the goal can also be specified, or if none is the CCA1 will operate in wander mode
        -has ability to trigger a return cycle to input sensory stages -- lower output value means ok
          with parsing of map, higher value means more incentive to send back to input sensory stages,
          which will trigger Instinctive and Learned Primitives including physics primitives,
          int, varies 0 -100
        '''
        print(self.nav_map, starting_point, goal) #avoid triggering pylint
        return 50

    def c_map_to_l_map(self, hierarchy_insertion: list)-> bool:
        '''CODE CLEAN UP -- DEPRECATED FROM MAPDATA CLASS TO THE NAVMOD CLASS
        l_map (for 'long term causal memory map) is created from c_map at present, but
          as code development proceeds c_map will be deprecated and l_map will be
          created directly -- l_map is not a list of maps but a hierarchy of maps
          all organized in the 6x6 format of nav_map and branching out
        -method writes directly to self.l_map
        -hierarchy_insertion guides where maps are inserted into other maps in converting
          c_map to l_map
        '''
        print('hierarchy_insertion value is: ', hierarchy_insertion)
        self.l_map = copy.deepcopy(self.c_map)
        print('c_map was copied to l_map, pending code development and c_map deprecation\n')
        return True
        