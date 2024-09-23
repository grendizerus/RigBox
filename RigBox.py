##############################################################################################################
#NAME: RigBox (Curves Tool)
#VERSION: See variable strRbVer below. The version history is now in the file : RigBox_Manual.html
#AUTHOR: David Saber (www.dreamcraftdigital.com), based on the code by Jennifer Conley.
#SCRIPTING LANGUAGE: Maya Python
#DATE OF LATEST VERSION: read the file : RigBox_Manual.html, section "Version History".
#LATEST VERSION BY: David Saber
#USAGE: This tool is used in Maya to help with control objects and icon creation, and other basic rig construction tasks. More info in the HTML file.
#MANUAL: it's now in the file : RigBox_Manual.html
#LINKS: Check author's link
#SUPPORT: Contact David Saber, see author above
#LATEST UPDATES: read the file : RigBox_Manual.html
#TODO: read the file : RigBox_Manual.html
##############################################################################################################



# Begin Content of original file : rr_main_curves.py

# Imports
# Import Pymel
# import pymel.core as pm
# Import Maya Python API
import maya.cmds as cmds
from functools import partial
# Commented out as all code is in a single file now
# import RigBox.rr_sub_curves_addAttributes
# import RigBox.rr_sub_curves_colorOptions
# import RigBox.rr_sub_curves_curveCreation
# import RigBox.rr_sub_curves_lockHide


# Global Variables: they are defined outside of any function in a program. They can be accessed and modified by any function or module in the program. How to Change a Global Variable in Function: A function accesses and modifies the value of global_var using the "global" keyword, then the variable can be re-set. Example : First line : def func(): , second line : global global_var , third line : global_var = "I have been modified."
strScriptName = "RigBox"
strRbVer = "4.03"
window_name_main = 'rr_control_window'
window_name_CurveCreation = 'Curve_Tool'
window_name_Color = 'rr_colors_win'
window_name_Attributes = 'rr_addAttrs_tool'
window_name_LockHide = 'lock_and_hide_window'
window_bgc = (.2, .2, .2)
element_bgc = (.45, .45, .45)
title_color = (0.860652, 0.759494, 1)
frame_backgroundColor = (0.655297, 0.405063, 1)
width_main = 325
width_curveCreation = 290
width_ColorAttrLockHide = 300
width_ColorAttrLockHide = 300
width_ColorAttrLockHide = 300
height = 600
cbw = 20
strCurrentControlCurveName = "" #Previously called : control
# Choose your colors in these 6 slots
colorL1C1=(1,0,0) #red
colorL1C2=(0,0,1) #blue
colorL2C1=(0.3,1,1) #sky
colorL2C2=(1,0.5,0) #orange
colorL3C1=(0.7,0.15,1) #purpel
colorL3C2=(1,1,0) #yellow
# Attribute Lists
finger_dropAttrs = ['Finger_Drops', 'Thumb_Drop', 'Pinky_Drop']
finger_spreadAttrs = ['Spreads', 'Thumb_Spread', 'Index_Spread', 'Middle_Spread', 'Ring_Spread', 'Pinky_Spread']
thumb_curlAttrs = ['Thumb_Curl', 'Thumb_Root', 'Thumb_Mid', 'Thumb_End']
index_curlAttrs = ['Index_Curl', 'Index_Root', 'Index_Mid', 'Index_End']
mid_curlAttrs = ['Mid_Curl', 'Mid_Root', 'Mid_Mid', 'Mid_End']
ring_curlAttrs = ['Ring_Curl', 'Ring_Root', 'Ring_Mid', 'Ring_End']
pinky_curlAttrs = ['Pinky_Curl', 'Pinky_Root', 'Pinky_Mid', 'Pinky_End']
toe_spreadAttrs = ['Spreads', 'Big_Spread', 'Index_Spread', 'Middle_Spread', 'Fourth_Spread', 'Pinky_Spread']
big_curlAttrs = ['Big_Curl', 'Big_Root', 'Big_Mid', 'Big_End']
fourth_curlAttrs = ['Fourth_Curl', 'Fourth_Root', 'Fourth_Mid', 'Fourth_End']
foot_raiseAttrs = ['Raises', 'Heel_Raise', 'Ball_Raise', 'Toe_Raise']


# GUI Creation Functions
def window_creation_Main():
    global window_object_Main
    strWinmainTitle = strScriptName + " V" + strRbVer
    if cmds.window(window_name_main, q=True, ex=True):
        cmds.deleteUI(window_name_main)
    if cmds.windowPref(window_name_main, ex=True):
        cmds.windowPref(window_name_main, r=True)
    window_object_Main = cmds.window(window_name_main, bgc=window_bgc, w=width_main, h=height, t=strWinmainTitle)
    gui_creation_Main()
    #old code : window_object_Main.show()
    cmds.showWindow(window_object_Main)

def gui_creation_Main():
    main = cmds.columnLayout()
    main_scroll = cmds.scrollLayout(h=height, w=width_main)

    create_frameLayout('Creation')
    gui_creation_curveCreation()
    cmds.setParent(main_scroll)

    create_frameLayout('Coloring')
    gui_creation_Color()
    cmds.setParent(main_scroll)

    create_frameLayout('Attributes')
    gui_creation_Attributes()
    cmds.setParent(main_scroll)

    create_frameLayout('Lock and Hide')
    gui_creation_LockHide()
    cmds.setParent(main_scroll)

def create_frameLayout(frame_name):
    cmds.frameLayout(l=frame_name, w=width_main - 25, cll=True, cl=True, bgc=frame_backgroundColor)
    
# End Content of original file : rr_main_curves.py



# Begin Content of original file : rr_sub_curves_curveCreation.py

"""
RigBox Reborn - Sub: Curve Creation

Author: Jennifer Conley
Date Modified: 11/23/12
Updates: David Saber
modified : v3, 2021-11

Description:
    A custom GUI to easily create commonly used control icons for rig construction.
    - Includes 2D, 3D, and text based curves.

    Provides features for:
    - Priming controls based on a selected transform node, or a hierarchy of nodes.
    - Naming control icons
    - Naming priming groups
    - Constraining selected transform node, with Parent or Orient constraint options

    The curve must be selected first, then the transform node. This selection order was
    choosen because it replicates actual parenting inside of Maya.
    

How to run:
    import rr_sub_curves_curveCreation
    rr_sub_curves_curveCreation.window_creation_CurveCreation()
"""

# Gui Creation
def window_creation_CurveCreation():
    if cmds.window(window_name_CurveCreation, q=True, ex=True):
        cmds.deleteUI(window_name_CurveCreation)

    if cmds.windowPref(window_name_CurveCreation, ex=True):
        cmds.windowPref(window_name_CurveCreation, r=True)

    global window_object_CurveCreation
    window_object_CurveCreation = cmds.window(window_name_CurveCreation, bgc=window_bgc, t='RigBox Reborn - Curve Creation', w=width_curveCreation)
    gui_creation_curveCreation()
    #Old code : window_object_CurveCreation.show()
    cmds.showWindow(window_object_CurveCreation)


def gui_creation_curveCreation():
    global main, naming_form, grouping_form, grouping_options_frame
    main = cmds.columnLayout()

    naming_form = cmds.formLayout()
    naming_title = title_creation_CurveCreation('Control Naming', naming_form)
    rename_col = rename_gui()
    ctrl_options_col = control_options_gui()

    cmds.formLayout(naming_form, e=True,
                  attachForm=[(ctrl_options_col, 'right', 5),
                              (ctrl_options_col, 'left', 5),
                              (rename_col, 'right', 5),
                              (rename_col, 'left', 5),
                              (naming_title, 'right', 5),
                              (naming_title, 'left', 5),
                              (naming_title, 'top', 5)],
                  attachControl=[(ctrl_options_col, 'top', 5, rename_col),
                                 (rename_col, 'top', 5, naming_title)])
    cmds.setParent(main)

    cmds.columnLayout(co=('left', 5))
    #Old code : grouping_options_frame = cmds.frameLayout(l='Grouping', en=False, w=width_curveCreation, cl=True, cll=True, bgc=frame_backgroundColor, cc=cmds.Callback(window_resize, -200))
    grouping_options_frame = cmds.frameLayout(l='Grouping', en=False, w=width_curveCreation, cl=True, cll=True, bgc=frame_backgroundColor, collapseCommand=partial(window_resize, -200))
    cmds.setParent(main)

    grouping_form = cmds.formLayout(p=grouping_options_frame)
    grouping_title = title_creation_CurveCreation('Group Naming', grouping_form)
    group_naming_col = group_naming_gui()
    grouping_instructions_title = title_creation_CurveCreation('Grouping Options', grouping_form)
    grouping_instructions_col = group_instructions_gui()
    grouping_options_col = grouping_options_gui()
    cmds.setParent(main)

    cmds.formLayout(grouping_form, e=True,
                  attachForm=[(grouping_options_col, 'left', 0),
                              (grouping_options_col, 'right', 0),
                              (grouping_instructions_col, 'left', 0),
                              (grouping_instructions_col, 'right', 0),
                              (grouping_instructions_title, 'left', 0),
                              (grouping_instructions_title, 'right', 0),
                              (group_naming_col, 'left', 0),
                              (group_naming_col, 'right', 0),
                              (grouping_title, 'left', 0),
                              (grouping_title, 'right', 0),
                              (grouping_title, 'top', 5), ],
                  attachControl=[(grouping_options_col, 'top', 5, grouping_instructions_col),
                                 (grouping_instructions_col, 'top', 5, grouping_instructions_title),
                                 (grouping_instructions_title, 'top', 5, group_naming_col),
                                 (group_naming_col, 'top', 5, grouping_title)])

    cmds.setParent(main)
    control_buttons_gui()


def rename_gui():
    main_col = cmds.columnLayout()
    cmds.rowColumnLayout(nc=3, cw=[(1, width_curveCreation / 3), (2, width_curveCreation / 3), (3, width_curveCreation / 3)])

    cmds.text(l='Prefix', w=width_curveCreation / 3)
    cmds.text(l='Name', w=width_curveCreation / 3)
    cmds.text(l='Suffix', w=width_curveCreation / 3)

    global ctrl_prefix_field, ctrl_name_field, ctrl_suffix_field

    ctrl_prefix_field = cmds.textField(w=width_curveCreation / 3)
    ctrl_name_field = cmds.textField(w=width_curveCreation / 3)
    ctrl_suffix_field = cmds.textField(w=width_curveCreation / 3)
    cmds.setParent(naming_form)

    return main_col


def control_options_gui():
    global snap_optionMenu, group_optionMenu

    main_col = cmds.columnLayout()
    cmds.rowColumnLayout(nc=3, cw=[(1, width_curveCreation / 2), (2, width_curveCreation / 2)])

    snap_optionMenu = cmds.optionMenu(w=width_curveCreation / 2, bgc=element_bgc)
    cmds.menuItem(l='Default')
    cmds.menuItem(l='Snap')

    group_optionMenu = cmds.optionMenu(w=width_curveCreation / 2, bgc=element_bgc, cc=unlock_grouping_frame)
    cmds.menuItem(l='Default')
    cmds.menuItem(l='Group')
    cmds.setParent(naming_form)

    return main_col


def group_naming_gui():
    sub_width = width_curveCreation - 5

    main_col = cmds.columnLayout(w=sub_width)
    cmds.rowColumnLayout(nc=3, cw=[(1, sub_width / 3), (2, sub_width / 3), (3, sub_width / 3)])

    cmds.text(l='Prefix', w=sub_width / 3)
    cmds.text(l='Name', w=sub_width / 3)
    cmds.text(l='Suffix', w=sub_width / 3)

    global grp1_prefix_field, grp1_name_field, grp1_suffix_field
    global grp2_prefix_field, grp2_name_field, grp2_suffix_field

    grp1_prefix_field = cmds.textField(w=sub_width / 3)
    grp1_name_field = cmds.textField(w=sub_width / 3)
    grp1_suffix_field = cmds.textField(w=sub_width / 3)

    grp2_prefix_field = cmds.textField(w=sub_width / 3)
    grp2_name_field = cmds.textField(w=sub_width / 3)
    grp2_suffix_field = cmds.textField(w=sub_width / 3)
    cmds.setParent(grouping_form)

    return main_col


def group_instructions_gui():
    sub_width = width_curveCreation - 5

    main_col = cmds.columnLayout(w=sub_width)
    cmds.text(l='Select a curve, then a joint.', w=sub_width)
    cmds.text(l="Click 'Apply' once tool options have been set.", w=sub_width)
    cmds.separator(w=sub_width, h=5)
    cmds.setParent(grouping_form)

    return main_col


def grouping_options_gui():
    global duplicate_optionMenu, hierarchy_optionMenu, constraint_optionMenu
    sub_width = width_curveCreation - 5

    main_col = cmds.columnLayout(w=sub_width)
    grouping_form = cmds.formLayout(w=sub_width)
    menu_col = cmds.rowColumnLayout(nc=3, cw=[(1, sub_width / 3), (2, sub_width / 3), (3, sub_width / 3)])

    duplicate_optionMenu = cmds.optionMenu(bgc=element_bgc, w=sub_width / 3)
    cmds.menuItem(l='Single')
    cmds.menuItem(l='Chain')

    hierarchy_optionMenu = cmds.optionMenu(bgc=element_bgc, w=sub_width / 3)
    cmds.menuItem(l='Default')
    cmds.menuItem(l='Hierarchy')

    constraint_optionMenu = cmds.optionMenu(bgc=element_bgc, w=sub_width / 3)
    cmds.menuItem(l='Default')
    cmds.menuItem(l='Orient')
    cmds.menuItem(l='Parent')
    cmds.setParent(grouping_form)

    apply_button_col = cmds.columnLayout(w=sub_width)
    cmds.separator(w=sub_width)
    cmds.button(l='Apply', w=sub_width, bgc=(.451, .451, .451), c=apply_button)
    cmds.separator(w=sub_width)

    cmds.formLayout(grouping_form, e=True,
                  attachForm=[(apply_button_col, 'bottom', 5),
                              (apply_button_col, 'right', 0),
                              (apply_button_col, 'left', 0),
                              (menu_col, 'top', 5),
                              (menu_col, 'right', 0),
                              (menu_col, 'left', 0)],
                  attachControl=[(apply_button_col, 'top', 5, menu_col)])

    return main_col


def control_buttons_gui():
    # This function draws the GUI part for the creations. It is called from the function gui_creation_curveCreation
    create_shapeButtons_gui()
    cmds.setParent(main)

    global char_form

    char_form = cmds.formLayout()

    text_title_col = title_creation_CurveCreation('Text Shapes', char_form)
    letter_col = letter_controls_gui()
    text_col = text_controls_gui()

    cmds.formLayout(char_form, e=True,
                  attachForm=[(letter_col, 'bottom', 5),
                              (text_col, 'bottom', 5),
                              (text_col, 'right', 5),
                              (letter_col, 'left', 5),
                              (text_title_col, 'left', 5),
                              (text_title_col, 'right', 5),
                              (text_title_col, 'top', 5)],
                  attachControl=[(text_col, 'left', 0, letter_col),
                                 (text_col, 'top', 5, text_title_col),
                                 (letter_col, 'top', 5, text_title_col), ],
                  attachPosition=[(text_col, 'left', 0, 49)])


def create_shapeButtons_gui():
    # This function draws the GUI part for the curves creations. It is called from the function : control_buttons_gui
    global twoD_form
    main_col = cmds.columnLayout(p=main)
    twoD_form = cmds.formLayout(nd=100)

    twoD_shapes_title = title_creation_CurveCreation('2D Shapes', twoD_form)
    twoD_controls_col = twoD_controls_gui()

    twoD_arrows_title = half_title_creation('2D Arrows', twoD_form)
    twoD_arrows_col = twoD_arrows_gui()
    threeD_title = half_title_creation('3D Shapes', twoD_form)
    threeD_controls_col = threeD_controls_gui()

    cmds.formLayout(twoD_form, e=True,
                  attachForm=[(threeD_controls_col, 'right', 5),
                              (twoD_arrows_col, 'left', 5),
                              (threeD_title, 'right', 5),
                              (twoD_arrows_title, 'left', 5),
                              (twoD_controls_col, 'right', 5),
                              (twoD_controls_col, 'left', 5),
                              (twoD_shapes_title, 'right', 5),
                              (twoD_shapes_title, 'left', 5),
                              (twoD_shapes_title, 'top', 5)],
                  attachControl=[(threeD_controls_col, 'left', 0, twoD_arrows_col),
                                 (threeD_controls_col, 'top', 5, threeD_title),
                                 (twoD_arrows_col, 'top', 5, twoD_arrows_title),
                                 (threeD_title, 'left', 0, twoD_arrows_title),
                                 (threeD_title, 'top', 5, twoD_controls_col),
                                 (twoD_arrows_title, 'top', 5, twoD_controls_col),
                                 (twoD_controls_col, 'top', 5, twoD_shapes_title), ],
                  attachPosition=[(threeD_title, 'left', 0, 49),
                                  (threeD_controls_col, 'left', 0, 49)])


def twoD_controls_gui():
    # This function draws the GUI part for the 2D shapes creations buttons. It is called from the function create_shapeButtons_gui
    print("RBDEBUG Function twoD_controls_gui, variable strCurrentControlCurveName, at begining: " + strCurrentControlCurveName)
    main_col = cmds.columnLayout(w=width_curveCreation)

    cmds.rowColumnLayout(w=width_curveCreation, nc=2, cw=[(width_curveCreation / 2), (width_curveCreation / 2)])
    cmds.button(l='Circle', bgc=element_bgc, w=width_curveCreation / 2, c=partial(create_shape_control, 'create_circle'))
    cmds.button(l='Square', bgc=element_bgc, w=width_curveCreation / 2, c=partial(create_shape_control, 'create_square'))
    cmds.button(l='Move All', bgc=element_bgc, w=width_curveCreation / 2, c=partial(create_shape_control, 'create_move_all'))
    cmds.button(l='Sun', bgc=element_bgc, w=width_curveCreation / 2, c=partial(create_shape_control, 'create_sun'))
    cmds.setParent(main_col)

    cmds.rowColumnLayout(w=width_curveCreation, nc=5,
                       cw=[(1, width_curveCreation / 5),
                           (2, width_curveCreation / 5),
                           (3, width_curveCreation / 5),
                           (4, width_curveCreation / 5),
                           (5, width_curveCreation / 5)])
    cmds.button(l='Pick', bgc=element_bgc, w=width_curveCreation / 5, c=partial(create_shape_control, 'create_pick'))
    cmds.button(l='Frame', bgc=element_bgc, w=width_curveCreation / 5, c=partial(create_shape_control, 'create_frame'))
    cmds.button(l='Triangle', bgc=element_bgc, w=width_curveCreation / 5, c=partial(create_shape_control, 'create_triangle'))
    cmds.button(l='Plus', bgc=element_bgc, w=width_curveCreation / 5, c=partial(create_shape_control, 'create_plus'))
    cmds.button(l='Swirl', bgc=element_bgc, w=width_curveCreation / 5, c=partial(create_shape_control, 'create_swirl'))
    cmds.setParent(twoD_form)

    return main_col


def twoD_arrows_gui():
    main_col = cmds.columnLayout(w=width_curveCreation / 2)

    cmds.rowColumnLayout(nc=2, w=width_curveCreation / 2, cw=[(1, width_curveCreation / 4), (2, width_curveCreation / 4)])
    cmds.button(l='Single', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_single_arrow'))
    cmds.button(l='Curved 1', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_curved_single_arrow'))
    cmds.setParent(main_col)

    cmds.rowColumnLayout(nc=2)
    cmds.button(l='Double', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_double_arrow'))
    cmds.button(l='Curved 2', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_curved_double_arrow'))
    cmds.button(l='Triple', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_triple_arrow'))
    cmds.button(l='Quad', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_quad_arrow'))
    cmds.setParent(twoD_form)

    return main_col


def threeD_controls_gui():
    main_col = cmds.columnLayout(w=width_curveCreation / 2)

    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=2, cw=[(1, width_curveCreation / 4), (2, width_curveCreation / 4)])
    cmds.button(l='Cube', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_cube'))
    cmds.button(l='Diamond', bgc=element_bgc, w=width_curveCreation / 4, c=partial(create_shape_control, 'create_diamond'))
    cmds.setParent(main_col)

    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=3, cw=[(1, width_curveCreation / 6), (2, width_curveCreation / 6), (3, width_curveCreation / 6)])
    cmds.button(l='Ring', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_ring'))
    cmds.button(l='Cone', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_cone'))
    cmds.button(l='Orb', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_orb'))

    cmds.button(l='Lever', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_lever'))
    cmds.button(l='Jack', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_jack'))
    cmds.button(l='Point', bgc=element_bgc, w=width_curveCreation / 6, c=partial(create_shape_control, 'create_pointer'))
    cmds.setParent(twoD_form)

    return main_col


def letter_controls_gui():
    main_col = cmds.columnLayout(w=width_curveCreation / 2)

    control_icon_list1 = ['E', 'K', 'L']
    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=2, cw=[(1, width_curveCreation / 4), (2, width_curveCreation / 4)])
    create_letter_button(control_icon_list1, width_curveCreation / 4)
    #Old code : cmds.button(l='R', w=width_curveCreation / 4, bgc=element_bgc, c=cmds.Callback(create_text_control, 'R'))
    cmds.button(l='R', w=width_curveCreation / 4, bgc=element_bgc, c=partial(create_text_control, 'R'))
    cmds.setParent(main_col)

    control_icon_list2 = ['C', 'H', 'S']
    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=4, cw=[(1, width_curveCreation / 8), (2, width_curveCreation / 8), (3, width_curveCreation / 8), (4, width_curveCreation / 8)])
    #Old code : cmds.button(l='B', w=width_curveCreation / 8, bgc=element_bgc, c=cmds.Callback(create_text_control, 'B'))
    cmds.button(l='B', w=width_curveCreation / 8, bgc=element_bgc, c=partial(create_text_control, 'B'))
    create_letter_button(control_icon_list2, width_curveCreation / 8)
    cmds.setParent(char_form)

    return main_col


def text_controls_gui():
    main_col = cmds.columnLayout(w=width_curveCreation / 2, )

    control_icon_list1 = ['Lf', 'Rt', 'Blends', 'Ik_Fk']
    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=2, cw=[(1, width_curveCreation / 4), (2, width_curveCreation / 4)])
    create_text_button(control_icon_list1, width_curveCreation / 4)
    cmds.setParent(main_col)

    cmds.rowColumnLayout(w=width_curveCreation / 2, nc=2, cw=[(1, width_curveCreation / 4), (2, width_curveCreation / 4)])
    control_icon_list2 = ['COG', 'GUI']
    create_text_button(control_icon_list2, width_curveCreation / 4)
    cmds.setParent(char_form)

    return main_col


# Gui Work Functions    
def create_letter_button(text_list, size):
    for individual_item in text_list:
        #Old code : cmds.button(l=individual_item, w=size, bgc=element_bgc, c=cmds.Callback(create_letter_control, individual_item))
        cmds.button(l=individual_item, w=size, bgc=element_bgc, c=partial(create_letter_control, individual_item))


def create_text_button(text_list, size):
    for individual_item in text_list:
        #Old code : cmds.button(l=individual_item, w=size, bgc=element_bgc, c=cmds.Callback(create_text_control, individual_item))
        cmds.button(l=individual_item, w=size, bgc=element_bgc, c=partial(create_text_control, individual_item))


def title_creation_CurveCreation(title, parent_layout):
    main = cmds.columnLayout()

    cmds.separator(w=width_curveCreation, h=5)
    cmds.text(l=title, w=width_curveCreation, bgc=title_color)
    cmds.separator(w=width_curveCreation, h=5)
    cmds.setParent(parent_layout)

    return main


def half_title_creation(title, parent_layout):
    main = cmds.columnLayout(w=(width_curveCreation / 2))

    cmds.separator(w=(width_curveCreation / 2), h=5)
    cmds.text(l=title, w=(width_curveCreation / 2), bgc=title_color)
    cmds.separator(w=(width_curveCreation / 2), h=5)
    cmds.setParent(parent_layout)

    return main


def window_resize(difference, *args):
    if cmds.window(window_name_CurveCreation, q=True, ex=True):
        current_height = window_object_CurveCreation.getHeight()
        height = current_height + difference
        window_object_CurveCreation.setHeight(height)


def unlock_grouping_frame(*args):
    #Old code : if group_optionMenu.getSelect() == 2:
    selected_value = cmds.optionMenu(group_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
        cmds.frameLayout(grouping_options_frame, e=True, en=True, cl=False)
    # cmds.frameLayout(grouping_options, en=True)
    else:
        if cmds.frameLayout(grouping_options_frame, q=True, cl=True):
            cmds.frameLayout(grouping_options_frame, e=True, en=False)
        else:
            window_resize(-200)
            cmds.frameLayout(grouping_options_frame, e=True, en=False, cl=True)


# Control Creation Functions
def run_function(function_name):
    exec(function_name + '()')


def create_shape_control(function_name, *args):
    #print("RBDEBUG at start of function create_shape_control, strCurrentControlCurveName: ", strCurrentControlCurveName)
    selected_value = cmds.optionMenu(duplicate_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (duplicate_optionMenu.getSelect()) == 2:
        snap_objects = select_hierarchy()
        parent_control = ''

        for i, indiv_object in enumerate(snap_objects):
            run_function(function_name)
            create_multiple_controls(strCurrentControlCurveName, indiv_object, parent_control, i)
            parent_control = strCurrentControlCurveName

        cmds.select(parent_control)

    else:
        snap_object = cmds.ls(sl=True)
        run_function(function_name)
        #old code : create_control(snap_object, strCurrentControlCurveName)
        create_control(snap_object)

    cmds.select(strCurrentControlCurveName)


def create_letter_control(var, *args):
    selected_value = cmds.optionMenu(duplicate_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (duplicate_optionMenu.getSelect()) == 2:
        snap_objects = select_hierarchy()
        parent_control = ''

        for i, indiv_object in enumerate(snap_objects):
            create_char(var)
            create_multiple_controls(strCurrentControlCurveName, indiv_object, parent_control, i)
            parent_control = strCurrentControlCurveName

        cmds.select(parent_control)

    else:
        snap_object = cmds.ls(sl=True)
        create_char(var)
        #old code : create_control(snap_object, strCurrentControlCurveName)
        create_control(snap_object)

    cmds.select(strCurrentControlCurveName)


def create_text_control(var, *args):
    selected_value = cmds.optionMenu(duplicate_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (duplicate_optionMenu.getSelect()) == 2:
        snap_objects = select_hierarchy()
        parent_control = ''

        for i, indiv_object in enumerate(snap_objects):
            create_text(var)
            create_multiple_controls(strCurrentControlCurveName, indiv_object, parent_control, i)
            parent_control = strCurrentControlCurveName

        cmds.select(parent_control)

    else:
        snap_object = cmds.ls(sl=True)
        create_text(var)
        #old code : create_control(snap_object, strCurrentControlCurveName)
        create_control(snap_object)

    cmds.select(strCurrentControlCurveName)


# Control Shape Functions
def create_circle():
    # This function creates a nurbs circle. It is called from withing the function twoD_controls_gui
    global strCurrentControlCurveName
    #print("RBDEBUG Function create_circle, variable strCurrentControlCurveName, at begining, atfer global var declaration: " + strCurrentControlCurveName)
    strCurrentControlCurveName = cmds.circle(n="Circle", nr=[0, 1, 0])[0]
    #print("RBDEBUG Function create_circle, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)
    

def create_square():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Square", d=1, p=[(-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1), (-1, 0, -1)], k=[0, 1, 2, 3, 4])


def create_move_all():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.circle(n="MoveAll", nr=[0, 1, 0])[0]

    arrow_list = []
    arrow_list.append(cmds.curve(d=1, p=[(1.75625, 0, 0.115973), (1.75625, 0, -0.170979), (2.114939, 0, -0.170979),
                                       (2.114939, 0, -0.314454), (2.473628, 0, -0.0275029), (2.114939, 0, 0.259448),
                                       (2.114939, 0, 0.115973), (1.75625, 0, 0.115973)], k=[0, 1, 2, 3, 4, 5, 6, 7]))
    arrow_list.append(cmds.curve(d=1, p=[(0.143476, 0, -1.783753), (0.143476, 0, -2.142442), (0.286951, 0, -2.142442),
                                       (0, 0, -2.501131), (-0.286951, 0, -2.142442), (-0.143476, 0, -2.142442),
                                       (-0.143476, 0, -1.783753), (0.143476, 0, -1.783753)],
                               k=[0, 1, 2, 3, 4, 5, 6, 7]))
    arrow_list.append(cmds.curve(d=1, p=[(-1.75625, 0, -0.170979), (-2.114939, 0, -0.170979), (-2.114939, 0, -0.314454),
                                       (-2.473628, 0, -0.0275029), (-2.114939, 0, 0.259448), (-2.114939, 0, 0.115973),
                                       (-1.75625, 0, 0.115973), (-1.75625, 0, -0.170979)], k=[0, 1, 2, 3, 4, 5, 6, 7]))
    arrow_list.append(cmds.curve(d=1, p=[(-0.143476, 0, 1.728747), (-0.143476, 0, 2.087436), (-0.286951, 0, 2.087436),
                                       (0, 0, 2.446125), (0.286951, 0, 2.087436), (0.143476, 0, 2.087436),
                                       (0.143476, 0, 1.728747), (-0.143476, 0, 1.728747)], k=[0, 1, 2, 3, 4, 5, 6, 7]))

    cmds.select(arrow_list)
    cmds.pickWalk(d='Down')
    cmds.select(strCurrentControlCurveName, tgl=True)
    cmds.parent(r=True, s=True)
    cmds.delete(arrow_list)
    cmds.xform(strCurrentControlCurveName, cp=True)


def create_sun():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.circle(n="Sun", s=16, nr=[0, 1, 0])[0]
    cmds.select((strCurrentControlCurveName + '.cv[1]'), (strCurrentControlCurveName + '.cv[3]'), (strCurrentControlCurveName + '.cv[5]'), (strCurrentControlCurveName + '.cv[7]'),
              (strCurrentControlCurveName + '.cv[9]'), (strCurrentControlCurveName + '.cv[11]'), (strCurrentControlCurveName + '.cv[13]'), (strCurrentControlCurveName + '.cv[15]'),
              (strCurrentControlCurveName + '.cv[17]'), (strCurrentControlCurveName + '.cv[19]'), r=True)
    cmds.scale(0.3, 0.3, 0.3, p=[0, 0, 0], r=True)
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=1, r=1, s=1, n=0)
    cmds.xform(strCurrentControlCurveName, cp=True)


def create_pick():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.circle(n="Pick", nr=[0, 1, 0])[0]
    cmds.move(0, 0, -1.108194, strCurrentControlCurveName + '.cv[5]', r=True)
    cmds.move(0, 0, 1.108194, strCurrentControlCurveName + '.cv[1]', r=True)
    cmds.move(-0.783612, 0, -0.783612, strCurrentControlCurveName + '.cv[6]', r=True)
    cmds.move(-0.783612, 0, 0.783612, strCurrentControlCurveName + '.cv[0]', r=True)
    cmds.move(-1.108194, 0, 0, strCurrentControlCurveName + '.cv[7]', r=True)


def create_frame():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Frame", d=1, p=[(-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-2, 0, -2), (2, 0, -2),
                               (1, 0, -1), (1, 0, 1), (2, 0, 2), (2, 0, -2), (2, 0, 2), (-2, 0, 2), (-1, 0, 1),
                               (-2, 0, 2), (-2, 0, -2)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


def create_triangle():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Trangle", d=1, p=[(-1, 0, 1), (1, 0, 1), (0, 0, -1), (-1, 0, 1)], k=[0, 1, 2, 3, ])


def create_plus():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Plus", d=1,
                       p=[(-1, 0, -3), (1, 0, -3), (1, 0, -1), (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3), (-1, 0, 3),
                          (-1, 0, 1), (-3, 0, 1), (-3, 0, -1), (-1, 0, -1), (-1, 0, -3)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    #cmds.scale(strCurrentControlCurveName, .33, .33, .33)
    cmds.scale(.33, .33, .33, strCurrentControlCurveName)
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)


def create_swirl():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Swirl", d=3, p=[(0, 0, 0.0360697), (-0.746816, 0, 1), (-2, 0, -0.517827), (0, 0, -2), (2, 0, 0),
                               (0.536575, 0, 2.809361), (-3.191884, 0, 1.292017), (-2.772303, 0, -2.117866),
                               (-0.771699, 0, -3), (1.229059, 0, -3), (3, 0, -1.863394), (3.950518, 0, 0.314344),
                               (3, 0, 3.347373), (0, 0, 4.152682)],
                       k=[0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11])


def create_single_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowOne", d=1, p=[(0, 1.003235, 0), (0.668823, 0, 0), (0.334412, 0, 0), (0.334412, -0.167206, 0),
                               (0.334412, -0.501617, 0), (0.334412, -1.003235, 0), (-0.334412, -1.003235, 0),
                               (-0.334412, -0.501617, 0), (-0.334412, -0.167206, 0), (-0.334412, 0, 0),
                               (-0.668823, 0, 0), (0, 1.003235, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    
def create_curved_single_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowCurved", d=1, p=[(0.548955, 0, 0.515808), (0.038166, 0, 0.479696), (0.313453, 0, 0.430468),
                               (0.229264, 0, 0.386448), (0.07214, 0, 0.274834), (-0.109301, 0, 0.050655),
                               (-0.223899, 0, -0.214146), (-0.263053, 0, -0.5), (-0.161797, 0, -0.5),
                               (-0.126399, 0, -0.241381), (-0.022676, 0, -0.001768), (0.141422, 0, 0.201014),
                               (0.283645, 0, 0.302034), (0.359798, 0, 0.341857), (0.301085, 0, 0.067734),
                               (0.548955, 0, 0.515808), ], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    cmds.xform(cp=True)


def create_double_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowDouble", d=1, p=[(0, 1, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (4, 1, 0), (5, 0, 0), (4, -1, 0),
                               (3, -2, 0), (3, -1, 0), (2, -1, 0), (1, -1, 0), (0, -1, 0), (-1, -1, 0), (-2, -1, 0),
                               (-3, -1, 0), (-3, -2, 0), (-4, -1, 0), (-5, 0, 0), (-4, 1, 0), (-3, 2, 0), (-3, 1, 0),
                               (-2, 1, 0), (-1, 1, 0), (0, 1, 0), ],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    cmds.xform(cp=True)
    cmds.scale(.2, .2, .2)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)

    
def create_curved_double_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowDoubleCurved", d=1, p=[(0.748955, 0, -1.015808), (0.238166, 0, -0.979696), (0.513453, 0, -0.930468),
                               (0.429264, 0, -0.886448), (0.27214, 0, -0.774834), (0.090699, 0, -0.550655),
                               (-0.023899, 0, -0.285854), (-0.063053, 0, 9.80765e-009), (-0.023899, 0, 0.285854),
                               (0.090699, 0, 0.550655), (0.27214, 0, 0.774834), (0.429264, 0, 0.886448),
                               (0.513453, 0, 0.930468), (0.238166, 0, 0.979696), (0.748955, 0, 1.015808),
                               (0.501085, 0, 0.567734), (0.559798, 0, 0.841857), (0.483645, 0, 0.802034),
                               (0.341422, 0, 0.701014), (0.177324, 0, 0.498232), (0.073601, 0, 0.258619),
                               (0.038203, 0, 8.87346e-009), (0.073601, 0, -0.258619), (0.177324, 0, -0.498232),
                               (0.341422, 0, -0.701014), (0.483645, 0, -0.802034), (0.559798, 0, -0.841857),
                               (0.501085, 0, -0.567734), (0.748955, 0, -1.015808)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                          26, 27, 28])
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)
    cmds.xform(cp=True)


def create_triple_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowTriple", d=1, p=[(-1, 1, 0), (-3, 1, 0), (-3, 2, 0), (-5, 0, 0), (-3, -2, 0), (-3, -1, 0), (-1, -1, 0),
                               (1, -1, 0), (3, -1, 0), (3, -2, 0), (5, 0, 0), (3, 2, 0), (3, 1, 0), (1, 1, 0),
                               (1, 3, 0), (2, 3, 0), (0, 5, 0), (-2, 3, 0), (-1, 3, 0), (-1, 1, 0), ],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
    cmds.xform(cp=True)
    cmds.xform(t=[0, -1.5, 0])
    cmds.scale(.2, .2, .2)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)


def create_quad_arrow():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="ArrowQuad", d=1,
                       p=[(1, 0, 1), (3, 0, 1), (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1), (1, 0, -1), (1, 0, -3),
                          (2, 0, -3), (0, 0, -5), (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1), (-3, 0, -2),
                          (-5, 0, 0), (-3, 0, 2), (-3, 0, 1), (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5), (2, 0, 3),
                          (1, 0, 3), (1, 0, 1), ],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    cmds.xform(cp=True)
    cmds.scale(.2, .2, .2)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)


def create_cube():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Cube", d=1, p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, -1, -1),
                               (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1),
                               (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


def create_diamond():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Diamond", d=1,
                       p=[(0, 1, 0), (-1, 0.00278996, 6.18172e-08), (0, 0, 1), (0, 1, 0), (1, 0.00278996, 0), (0, 0, 1),
                          (1, 0.00278996, 0), (0, 0, -1), (0, 1, 0), (0, 0, -1), (-1, 0.00278996, 6.18172e-08),
                          (0, -1, 0), (0, 0, -1), (1, 0.00278996, 0), (0, -1, 0), (0, 0, 1)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


def create_ring():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Ring", d=1, p=[(-0.707107, 0.0916408, 0.707107), (0, 0.0916408, 1), (0, -0.0916408, 1),
                               (-0.707107, -0.0916408, 0.707107), (-0.707107, 0.0916408, 0.707107), (-1, 0.0916408, 0),
                               (-1, -0.0916408, 0), (-0.707107, -0.0916408, 0.707107), (-1, -0.0916408, 0),
                               (-0.707107, -0.0916408, -0.707107), (-0.707107, 0.0916408, -0.707107),
                               (-1, 0.0916408, 0), (-0.707107, 0.0916408, -0.707107), (0, 0.0916408, -1),
                               (0, -0.0916408, -1), (-0.707107, -0.0916408, -0.707107),
                               (-0.707107, 0.0916408, -0.707107), (-0.707107, -0.0916408, -0.707107),
                               (0, -0.0916408, -1), (0.707107, -0.0916408, -0.707107), (0.707107, 0.0916408, -0.707107),
                               (0, 0.0916408, -1), (0.707107, 0.0916408, -0.707107), (1, 0.0916408, 0),
                               (1, -0.0916408, 0), (0.707107, -0.0916408, -0.707107), (1, -0.0916408, 0),
                               (0.707107, -0.0916408, 0.707107), (0.707107, 0.0916408, 0.707107), (1, 0.0916408, 0),
                               (0.707107, 0.0916408, 0.707107), (0, 0.0916408, 1), (0, -0.0916408, 1),
                               (0.707107, -0.0916408, 0.707107)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                          26, 27, 28, 29, 30, 31, 32, 33])


def create_cone():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Cone", d=1, p=[(-0.5, -1, 0.866025), (0, 1, 0), (0.5, -1, 0.866025), (-0.5, -1, 0.866025),
                               (-1, -1, -1.5885e-07), (0, 1, 0), (-1, -1, -1.5885e-07), (-0.5, -1, -0.866026),
                               (0, 1, 0), (0.5, -1, -0.866025), (-0.5, -1, -0.866026), (0.5, -1, -0.866025), (0, 1, 0),
                               (1, -1, 0), (0.5, -1, -0.866025), (1, -1, 0), (0.5, -1, 0.866025)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])


def create_orb():
    global strCurrentControlCurveName
    #print("RBDEBUG Function create_orb, variable strCurrentControlCurveName, at begining, atfer global var declaration: " + strCurrentControlCurveName)
    strCurrentControlCurveName = cmds.circle(n="OrbBase", nr=(0, 1, 0))[0]
    # Next line : creation of an array of objects
    circle_list = []
    # Next lines : Using square brackets: Extend() vs Append(): append() creates a list inside a list. extend() adds multiple values individually
    circle_list.extend(cmds.duplicate(rr=True))
    cmds.xform(ro=(90, 0, 0))
    circle_list.extend(cmds.duplicate(rr=True))
    cmds.xform(ro=(90, 90, 0))
    circle_list.extend(cmds.duplicate(rr=True))
    cmds.xform(ro=(90, 45, 0))
    circle_list.extend(cmds.duplicate(rr=True))
    cmds.xform(ro=(90, -45, 0))
    # print("RBDEBUG circle_list array: ", circle_list)
    # print("RBDEBUG circle_list array, item 0: ", circle_list[0])
    cmds.select(circle_list)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)
    cmds.pickWalk(d='down')
    cmds.select(strCurrentControlCurveName, tgl=True)
    cmds.parent(r=True, s=True)
    cmds.delete(circle_list)
    cmds.xform(strCurrentControlCurveName, cp=True)
    # Select the object you want to rename
    cmds.select(strCurrentControlCurveName)
    # Check if an object is selected
    if cmds.ls(sl=True):
        old_name = strCurrentControlCurveName
        new_name = "Orb"
        # Rename the object
        cmds.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}")
    else:
        print("No object selected.")
    strCurrentControlCurveName = new_name
    print("RBDEBUG Function create_lever, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)


def create_lever():
    global strCurrentControlCurveName
    print("RBDEBUG Function create_lever, variable strCurrentControlCurveName, at begining, atfer global var declaration: " + strCurrentControlCurveName)
    line = cmds.curve(n="LeverLine", d=1, p=[(0, -1, 0), (0, -2, 0), (0, -3, 0), (0, -4, 0), (0, -5, 0)], k=[0, 1, 2, 3, 4])
    create_orb()

    cmds.select(line, r=True)
    cmds.pickWalk(d='down')
    cmds.select(strCurrentControlCurveName, tgl=True)
    cmds.parent(r=True, s=True)

    cmds.delete(line)
    cmds.xform(strCurrentControlCurveName, rp=[0, -5, 0], sp=[0, -5, 0])
    cmds.xform(strCurrentControlCurveName, t=[0, 5, 0])
    cmds.scale(.2, .2, .2)
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)
    # Select the object you want to rename
    cmds.select(strCurrentControlCurveName)
    # Check if an object is selected
    if cmds.ls(sl=True):
        old_name = strCurrentControlCurveName
        new_name = "Lever"
        # Rename the object
        cmds.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}")
    else:
        print("No object selected.")
    strCurrentControlCurveName = new_name
    print("RBDEBUG Function create_lever, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)


def create_jack():
    global strCurrentControlCurveName
    cross = cmds.curve(n="JackBase", d=1, p=[(0, 0, 0.75), (0, 0, 0), (0, 0, -0.75), (0, 0, 0), (0.75, 0, 0), (0, 0, 0), (-0.75, 0, 0),
                             (0, 0, 0), (0, 0.75, 0), (0, 0, 0), (0, -0.75, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    create_diamond()
    cmds.scale(.3, .3, .3)
    cmds.xform(t=[0, 0, 1])
    diamond_list = []
    diamond_list.extend(cmds.duplicate(rr=True))
    cmds.xform(t=[1, 0, 0])
    diamond_list.extend(cmds.duplicate(rr=True))
    cmds.xform(t=[-1, 0, 0])
    diamond_list.extend(cmds.duplicate(rr=True))
    cmds.xform(t=[0, -1, 0])
    diamond_list.extend(cmds.duplicate(rr=True))
    cmds.xform(t=[0, 1, 0])
    diamond_list.extend(cmds.duplicate(rr=True))
    cmds.xform(t=[0, 0, -1])
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)
    cmds.select(diamond_list, r=True)
    cmds.select(cross, tgl=True)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)
    cmds.pickWalk(d='down')
    cmds.select(strCurrentControlCurveName, tgl=True)
    cmds.parent(s=True, r=True)
    cmds.xform(strCurrentControlCurveName, cp=True)
    cmds.delete(diamond_list)
    cmds.delete(cross)
    # Select the object you want to rename
    cmds.select(strCurrentControlCurveName)
    # Check if an object is selected
    if cmds.ls(sl=True):
        old_name = strCurrentControlCurveName
        new_name = "Jack"
        # Rename the object
        cmds.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}")
    else:
        print("No object selected.")
    strCurrentControlCurveName = new_name
    print("RBDEBUG Function create_Jack, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)

def create_pointer():
    global strCurrentControlCurveName
    strCurrentControlCurveName = cmds.curve(n="Pointer", d=1, p=[(0, 1.003235, 0), (0.668823, 0, 0), (0.334412, 0, 0), (0.334412, -0.167206, 0),
                               (0.334412, -0.501617, 0), (0.334412, -1.003235, 0), (-0.334412, -1.003235, 0),
                               (-0.334412, -0.501617, 0), (-0.334412, -0.167206, 0), (-0.334412, 0, 0),
                               (-0.668823, 0, 0), (0, 1.003235, 0), (0, 0, -0.668823), (0, 0, -0.334412),
                               (0, -0.167206, -0.334412), (0, -0.501617, -0.334412), (0, -1.003235, -0.334412),
                               (0, -1.003235, 0.334412), (0, -0.501617, 0.334412), (0, -0.167206, 0.334412),
                               (0, 0, 0.334412), (0, 0, 0.668823), (0, 1.003235, 0)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])


def create_char(var):
    # This function draws letters in the viewport. It is called from 
    global strCurrentControlCurveName
    print("RBDEBUG Function create_char, variable var, at begin: " + var)
    print("RBDEBUG Function create_char, variable strCurrentControlCurveName, at begin: " + strCurrentControlCurveName)
    cmds.textCurves(n=var, ch=0, f='Times New Roman', t=var)
    cmds.ungroup()
    cmds.ungroup()
    strCurrentControlCurveName = cmds.ls(sl=True)[0]
    cmds.xform(cp=True)
    cmds.rename(strCurrentControlCurveName, var)
    strCurrentControlCurveName = var
    print("RBDEBUG Function create_char, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)


def create_text(var):
    # This function draws letters in the viewport. It is called from 
    global strCurrentControlCurveName
    print("RBDEBUG Function create_text, variable var, at begin: " + var)
    cmds.textCurves(n=var, ch=0, f='Times New Roman', t=var)
    cmds.ungroup()
    cmds.ungroup()

    curves = cmds.ls(sl=True)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    shapes = curves[1:]
    cmds.select(shapes, r=True)
    cmds.pickWalk(d='Down')
    cmds.select(curves[0], tgl=True)
    cmds.parent(r=True, s=True)
    cmds.pickWalk(d='up')
    strCurrentControlCurveName = cmds.ls(sl=True)[0]
    cmds.delete(shapes)
    cmds.xform(cp=True)
    cmds.xform(ws=True, t=[0, 0, 0])
    cmds.rename(strCurrentControlCurveName, var)
    strCurrentControlCurveName = var
    print("RBDEBUG Function create_text, variable strCurrentControlCurveName, at end: " + strCurrentControlCurveName)


# Work Functions
#Old code : def rename_control(strCurrentControlCurveName, i):
def rename_control(i):
    global strCurrentControlCurveName
    Renamed = strCurrentControlCurveName
    print("RBDEBUG at start of function rename_control, strCurrentControlCurveName: ", strCurrentControlCurveName)
    # Old codes : prefix = ctrl_prefix_field.getText()
    prefix = cmds.textField(ctrl_prefix_field, q=True, text=True)
    name = cmds.textField(ctrl_name_field, q=True, text=True)
    suffix = cmds.textField(ctrl_suffix_field, q=True, text=True)
    # rename(old name, new name)
    # next line : prevent increment if only 1 object is created
    if name != '':
        if i < 0 :
            cmds.rename(Renamed, name)
            Renamed = name
        else :
            cmds.rename(Renamed, name + str(i))
            Renamed = name + str(i)
    if prefix != '':
        cmds.rename(Renamed, prefix + '_' + Renamed)
        Renamed = prefix + '_' + Renamed
    if suffix != '':
        cmds.rename(Renamed, Renamed + '_' + suffix)
        Renamed = Renamed + '_' + suffix
    strCurrentControlCurveName = Renamed


def select_hierarchy():
    cmds.select(hi=True)
    snap_objects = cmds.ls(sl=True)
    snap_objects.pop(-1)

    return snap_objects


# old code : def create_control(snap_object, strCurrentControlCurveName):
def create_control(snap_object):
    snap_to_object(strCurrentControlCurveName, snap_object)
    print("RBDEBUG create_control : Value of strCurrentControlCurveName before rename: " + strCurrentControlCurveName)
    #old code : rename_control(strCurrentControlCurveName, 0)
    rename_control(-1)
    print("RBDEBUG create_control : Value of strCurrentControlCurveName after rename: " + strCurrentControlCurveName)
    create_grouping(strCurrentControlCurveName, snap_object)
    freeze_control(strCurrentControlCurveName)
    create_constraint(snap_object, strCurrentControlCurveName)


def create_multiple_controls(strCurrentControlCurveName, indiv_object, parent_control, i):
    snap_to_object(strCurrentControlCurveName, indiv_object)
    #old code : rename_control(strCurrentControlCurveName, i)
    rename_control(i)

    null_group = create_grouping(strCurrentControlCurveName, indiv_object)

    check_hierarchy(null_group, parent_control)
    freeze_control(strCurrentControlCurveName)
    create_constraint(indiv_object, strCurrentControlCurveName)


def freeze_control(strCurrentControlCurveName):
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)


def zero_control(strCurrentControlCurveName):
    cmds.xform(strCurrentControlCurveName, t=(0, 0, 0), ro=(0, 0, 0))


def snap_to_object(strCurrentControlCurveName, snap_object):
    selected_value = cmds.optionMenu(snap_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (snap_optionMenu.getSelect()) == 2:
        constraint = cmds.parentConstraint(snap_object, strCurrentControlCurveName)
        cmds.delete(constraint)
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)


def move_to_object(strCurrentControlCurveName, snap_object):
    selected_value = cmds.optionMenu(snap_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (snap_optionMenu.getSelect()) == 2:
        constraint = cmds.pointConstraint(snap_object, strCurrentControlCurveName, mo=False)
        cmds.delete(constraint)
    cmds.makeIdentity(strCurrentControlCurveName, apply=True, t=True, r=True, s=True)


def create_grouping(strCurrentControlCurveName, snap_object):
    selected_value = cmds.optionMenu(group_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if (group_optionMenu.getSelect()) == 2:
        pivot = cmds.xform(snap_object, q=True, ws=True, rp=True)

        cmds.select(strCurrentControlCurveName, snap_object, r=True)
        cmds.parent()
        grp2 = cmds.group()
        cmds.xform(ws=True, rp=pivot)
        grp1 = cmds.group()
        cmds.xform(ws=True, rp=pivot)
        cmds.parent(w=True)

        rename_groups(grp1, grp2, strCurrentControlCurveName)

        return grp1


def rename_groups(grp1, grp2, strCurrentControlCurveName):
    #Old codes : grp1_prefix = grp1_prefix_field.getText()
    grp1_prefix = cmds.textField(grp1_prefix_field, q=True, text=True)
    grp1_name = cmds.textField(grp1_name_field, q=True, text=True)
    grp1_suffix = cmds.textField(grp1_suffix_field, q=True, text=True)

    if grp1_name == '':
        cmds.rename(grp1, strCurrentControlCurveName)
    else:
        cmds.rename(grp1, grp1_name)

    if grp1_prefix != '':
        cmds.rename(grp1, grp1_prefix + '_' + grp1)

    if grp1_suffix != '':
        cmds.rename(grp1, grp1 + '_' + grp1_suffix)

    #Old codes : grp2_prefix = grp2_prefix_field.getText()
    grp2_prefix = cmds.textField(grp2_prefix_field, q=True, text=True)
    grp2_name = cmds.textField(grp2_name_field, q=True, text=True)
    grp2_suffix = cmds.textField(grp2_suffix_field, q=True, text=True)

    if grp2_name == '':
        cmds.rename(grp2, strCurrentControlCurveName)
    else:
        cmds.rename(grp2, grp2_name)

    if grp2_prefix != '':
        cmds.rename(grp2, grp2_prefix + '_' + grp2)

    if grp2_suffix != '':
        cmds.rename(grp2, grp2 + '_' + grp2_suffix)


def create_constraint(constrained_object, strCurrentControlCurveName):
    selected_value = cmds.optionMenu(group_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if group_optionMenu.getSelect() == 2:
        selected_value_cns = cmds.optionMenu(constraint_optionMenu, q=True, sl=True)
        #print("RBDEBUG : Selected value: ", selected_value_cns)
        if selected_value_cns == 2:
        #Old code : if constraint_optionMenu.getSelect() == 2:
            cmds.orientConstraint(strCurrentControlCurveName, constrained_object)
        elif selected_value_cns == 3:
        #old code : elif constraint_optionMenu.getSelect() == 3:
            cmds.parentConstraint(strCurrentControlCurveName, constrained_object, mo=True)


def check_hierarchy(null_group, parent_control):
    selected_value = cmds.optionMenu(hierarchy_optionMenu, q=True, sl=True)
    #print("RBDEBUG : Selected value: ", selected_value)
    if selected_value == 2:
    #Old code : if hierarchy_optionMenu.getSelect() == 2:
        if parent_control != '':
            cmds.parent(null_group, parent_control)


def apply_button(*args):
    selection = cmds.ls(sl=True)
    selected_value = cmds.optionMenu(duplicate_optionMenu, q=True, sl=True)
    #old code : if duplicate_optionMenu.getSelect() == 1:
    if selected_value == 1:
        applyButton_singleObject(selection)
    elif selected_value == 2:
        applyButton_objectChain(selection)


def applyButton_singleObject(selection):
    null_grp = create_grouping(selection[0], selection[1])
    freeze_control(selection[0])
    create_constraint(selection[1], selection[0])

    return null_grp


def applyButton_objectChain(selection):
    cmds.select(selection[1], hi=True)
    object_chain = cmds.ls(sl=True)
    object_chain.pop(-1)
    parent_control = ''

    curve_list = []
    nullGrp_list = []

    for each in object_chain:
        if each == object_chain[0]:
            strCurrentControlCurveName = selection[0]
            curve_list.append(strCurrentControlCurveName)

            applyButton_singleObject(selection)
            cmds.select(strCurrentControlCurveName, r=True)
            parent_control = strCurrentControlCurveName
        else:
            curve_list.append(strCurrentControlCurveName)

            null_grp = create_grouping(strCurrentControlCurveName, each)
            nullGrp_list.append(null_grp)
            cmds.select(strCurrentControlCurveName, r=True)

            zero_control(strCurrentControlCurveName)
            create_constraint(each, strCurrentControlCurveName)
            parent_control = strCurrentControlCurveName

        cmds.duplicate(strCurrentControlCurveName)
        strCurrentControlCurveName = cmds.ls(sl=True)[0]

        cmds.delete(strCurrentControlCurveName)
    create_hierarchy(nullGrp_list, curve_list)


def create_hierarchy(nullGrp_list, curve_list):
    selected_value = cmds.optionMenu(hierarchy_optionMenu, q=True, sl=True)
    #old code : if hierarchy_optionMenu.getSelect() == 2:
    if selected_value == 2:
        curve_list.pop(-1)
    curve_list.reverse()
    nullGrp_list.reverse()
    for i, each in enumerate(nullGrp_list):
        cmds.parent(nullGrp_list[i], curve_list[i])
        cmds.select(cl=True)

# End Content of original file : rr_sub_curves_curveCreation.py



# Begin Content of original file : rr_sub_curves_colorOptions.py

"""
Rigbox Reborn - Sub: Color Options

Author: Jennifer Conley
Date Modified: 11/23/12
Script updated: check rr_ReadMe.txt

Description:
    A script to quickly color control icons for a rig. Able to be run on a selection.
    Also has options for templating an object.

How to run:
    import rr_sub_curves_colorOptions
    rr_sub_curves_colorOptions.window_creation_Color()
    
    More info in the text file : rr_ReadMe.txt
"""

# Gui Creation
def window_creation_Color():
    if cmds.window(window_name_Color, q=True, ex=True):
        cmds.deleteUI(window_name_Color)

    if cmds.windowPref(window_name_Color, ex=True):
        cmds.windowPref(window_name_Color, r=True)

    window_object_Color = cmds.window(window_name_Color, bgc=window_bgc, w=width_ColorAttrLockHide, t='RigBox Reborn - Color Options')
    gui_creation_Color()
    #Old code : window_object_Color.show()
    cmds.showWindow(window_object_Color)


def gui_creation_Color():
    main = cmds.columnLayout(w=width_ColorAttrLockHide)
    main_form = cmds.formLayout(nd=100, w=width_ColorAttrLockHide)

    color_options_title = cmds.columnLayout(w=width_ColorAttrLockHide)
    create_grouping_title = cmds.columnLayout()
    # cmds.separator(w=width_ColorAttrLockHide-15, h=5)
    # cmds.text(l='Color Options', w=width_ColorAttrLockHide-15, bgc=(.66, 1, .66))
    cmds.separator(w=width_ColorAttrLockHide - 15, h=5)
    cmds.text(w=width_ColorAttrLockHide, l='Select the curves for coloring.')
    cmds.text(w=width_ColorAttrLockHide, l='Then click a color.')
    cmds.separator(w=width_ColorAttrLockHide - 15, h=5)
    cmds.setParent(main_form)
    
    color_options = cmds.columnLayout()
    cmds.rowColumnLayout(nc=2)
    #Old code, for the 6 following lines : cmds.button(l='', w=90, bgc=colorL1C1, c=cmds.Callback(rr_RGBcolorCurves_buttons_v2, color=colorL1C1))
    cmds.button(l='Red', w=90, bgc=colorL1C1, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL1C1))
    cmds.button(l='Blue', w=90, bgc=colorL1C2, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL1C2))
    cmds.button(l='Sky', w=90, bgc=colorL2C1, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL2C1))
    cmds.button(l='Orange', w=90, bgc=colorL2C2, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL2C2))
    cmds.button(l='Purple', w=90, bgc=colorL3C1, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL3C1))
    cmds.button(l='Yellow', w=90, bgc=colorL3C2, c=partial(rr_RGBcolorCurves_buttons_v2, color=colorL3C2))
    cmds.setParent(main_form)

    divider = cmds.columnLayout()
    cmds.separator(h=70, hr=False)
    cmds.setParent(main_form)

    template_options = cmds.columnLayout(w=width_ColorAttrLockHide)
    cmds.button(l='Template Attr', bgc=element_bgc, w=95, c=rr_template_attr)
    cmds.button(l='Template', bgc=element_bgc, w=95, c=rr_template_object)
    cmds.button(l='Untemplate', bgc=element_bgc, w=95, c=rr_untemplate)
    cmds.setParent(main_form)

    cmds.formLayout(main_form, e=True,
                  attachForm=[(divider, 'bottom', 5),
                              (color_options, 'bottom', 5),
                              (color_options, 'left', 5),
                              (template_options, 'bottom', 5),
                              (color_options_title, 'right', 5),
                              (color_options_title, 'left', 5),
                              (color_options_title, 'top', 5)],
                  attachControl=[(divider, 'top', 2, color_options_title),
                                 (divider, 'right', 0, template_options),
                                 (divider, 'left', 0, color_options),
                                 (color_options, 'top', 2, color_options_title),
                                 (template_options, 'left', 5, color_options),
                                 (template_options, 'top', 2, color_options_title)],
                  attachPosition=[(color_options_title, 'right', 2, 60)])


# Work Functions
    
def rr_RGBcolorCurves_buttons_v2(*args, color = (1,1,1)):
    selection = cmds.ls(sl=True)
    for n in selection:
        #print("RBDEBUG : n: ", n)
        cmds.setAttr(n + '.overrideEnabled', True)
        cmds.setAttr(n + '.overrideRGBColors', 1)
        cmds.setAttr(n + ".overrideColorRGB", color[0], color[1], color[2]) 
    print("Selection's RGB color has been changed.")

def rr_template_object(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        cmds.setAttr(individual_object + '.template', k=True)
        cmds.setAttr(individual_object + '.template', 1)

    print("Selection has been templated.")


def rr_untemplate(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        cmds.setAttr(individual_object + '.template', 0)

    print("Selection has been untemplated.")


def rr_template_attr(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        cmds.setAttr(individual_object + '.template', k=True)

    print("Selection has had the template attribute set to 'keyable'.")

# End Content of original file : rr_sub_curves_colorOptions.py



# Begin Content of original file : rr_sub_curves_addAttributes.py

"""
RigBox Reborn - Sub: Add Attributes Tool

Author: Jennifer Conley
Date Modified: 11/23/12

Description:
    A custom GUI to easily add common attributes to objects.
    
    Allows for additonal, custom attributes, to be added to objects
    without having to navigate to other windows.
    
How to run:
    import rr_sub_curves_addAttributes
    rr_sub_curves_addAttributes.window_creation_Attributes()
"""

# Gui Functions
def window_creation_Attributes():
    if cmds.window(window_name_Attributes, q=True, ex=True):
        cmds.deleteUI(window_name_Attributes)
    if cmds.windowPref(window_name_Attributes, ex=True):
        cmds.windowPref(window_name_Attributes, r=True)

    window_object_Attributes = cmds.window(window_name_Attributes, bgc=window_bgc, t='RigBox Reborn - Add Attribute', w=width_ColorAttrLockHide)
    gui_creation_Attributes()
    #Old code : window_object_Attributes.show()
    cmds.showWindow(window_object_Attributes)


def gui_creation_Attributes():
    main = cmds.columnLayout(w=width_ColorAttrLockHide)
    main_form = cmds.formLayout(nd=100, w=width_ColorAttrLockHide)

    preset_options_column = cmds.columnLayout(w=width_ColorAttrLockHide)
    title_creation_Attributes('Preset Options')
    preset_options()
    cmds.setParent(main_form)

    custom_options_column = cmds.columnLayout(w=width_ColorAttrLockHide)
    title_creation_Attributes('Custom Options')
    custom_options()
    cmds.setParent(main_form)

    cmds.formLayout(main_form, e=True,
                  attachForm=[(custom_options_column, 'left', 5), (custom_options_column, 'right', 5),
                              (custom_options_column, 'bottom', 5), (preset_options_column, 'left', 5),
                              (preset_options_column, 'right', 5), (preset_options_column, 'top', 5)],
                  attachControl=[(custom_options_column, 'top', 2, preset_options_column)])


def title_creation_Attributes(title):
    cmds.columnLayout(w=width_ColorAttrLockHide)
    cmds.separator(w=width_ColorAttrLockHide - 15, h=5)
    cmds.text(l=title, w=width_ColorAttrLockHide - 15, bgc=title_color)
    cmds.separator(w=width_ColorAttrLockHide - 15, h=5)


def preset_options():
    main = cmds.columnLayout(w=width_ColorAttrLockHide)

    cmds.rowColumnLayout(nc=2, w=width_ColorAttrLockHide)
    cmds.button(w=141, bgc=element_bgc, l='Ik Foot', c=add_ikFootAttrs)
    cmds.button(w=141, bgc=element_bgc, l='Foot Switch', c=add_footSwitchAttrs)
    cmds.button(w=141, bgc=element_bgc, l='Ik Hand', c=add_ikHandAttrs)
    cmds.button(w=141, bgc=element_bgc, l='Hand Switch', c=add_handSwitchAttrs)
    cmds.setParent(main)

    cmds.rowColumnLayout(nc=3, w=width_ColorAttrLockHide)
    cmds.button(w=94, bgc=element_bgc, l='Cog', c=add_cogAttrs)
    cmds.button(w=94, bgc=element_bgc, l='Head', c=add_headAttrs)
    cmds.button(w=94, bgc=element_bgc, l='Eye', c=add_eyeAttrs)
    cmds.setParent(main)


def custom_options():
    global attributeType_radioGrp, attribute_nameField, attribute_minField, attribute_maxField
    main = cmds.columnLayout()
    attributeType_radioGrp = cmds.radioButtonGrp(cc=field_display, sl=1, nrb=4, cw4=(75, 75, 75, 75),
                                               la4=('Float', 'Integer', 'Boolean', 'Sep'))

    cmds.separator(w=width_ColorAttrLockHide - 15, h=10)
    cmds.rowColumnLayout(nc=4, w=width_ColorAttrLockHide)
    attribute_nameField = cmds.textField(w=71, ann='Attribute Name', tx='Name')
    attribute_minField = cmds.floatField(w=71, ann='Attribute Min', v=-360, pre=1)
    attribute_maxField = cmds.floatField(w=71, ann='Attribute Max', v=360, pre=1)
    cmds.button(l='Create', bgc=element_bgc, w=71, c=create_attr)
    cmds.setParent(main)


# Gui Work Functions    
def field_display(*args):
    attr_value = cmds.radioButtonGrp(attributeType_radioGrp, q=True, sl=True)
    #old code : attr_value = attributeType_radioGrp.getSelect()    

    if attr_value == 1:
        attribute_minField.setEnable(True)
        attribute_maxField.setEnable(True)

    elif attr_value == 2:
        attribute_minField.setEnable(True)
        attribute_maxField.setEnable(True)

    elif attr_value == 3:
        attribute_minField.setEnable(False)
        attribute_maxField.setEnable(False)

    else:
        attribute_minField.setEnable(False)
        attribute_maxField.setEnable(False)

    print('Attribut Creation GUI has been updated.')


# Work Functions
def add_cogAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Adv_Back')
        cmds.addAttr(individual_object, ln='Back_Ctrls', at='enum', en='Fk_Ctrls:Ik_Ctrls:Both:None', k=True)

        create_separatorAttr(individual_object, 'Other')
        cmds.addAttr(individual_object, ln='Res', at='enum', en='Low:Proxy:High', k=True)
        create_boolAttr(individual_object, 'Auto_Hips')


def add_eyeAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Control_Visibility')
        create_boolAttr(individual_object, 'Indiv_Ctrls')


def add_headAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Control_Visibility')
        create_boolAttr(individual_object, 'Face_Ctrls')
        create_boolAttr(individual_object, 'Eye_Ctrls')


def add_ikFootAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Foot_SDKs')

        create_floatAttr(individual_object, 'Foot_Roll', -10, 10)
        create_floatAttr(individual_object, 'Bank', -360, 360)

        create_curlAttrs(individual_object, foot_raiseAttrs)

        create_separatorAttr(individual_object, 'Grinds')
        create_floatAttr(individual_object, 'Heel_Grind', -360, 360)
        create_floatAttr(individual_object, 'Toe_Grind', -360, 360)

        create_separatorAttr(individual_object, 'Knee_Pv')
        create_floatAttr(individual_object, 'Knee', -360, 360)
        create_floatAttr(individual_object, 'Offset', -360, 360)

        create_separatorAttr(individual_object, 'Space_Switching')
        create_floatAttr(individual_object, 'Cog', -360, 360)
        create_floatAttr(individual_object, 'Locator', -360, 360)


def add_ikHandAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Space_Switching')
        create_floatAttr(individual_object, 'Head', 0, 10)
        create_floatAttr(individual_object, 'Back', 0, 10)
        create_floatAttr(individual_object, 'Hips', 0, 10)
        create_floatAttr(individual_object, 'Locator', 0, 10)


def add_footSwitchAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Foot_SDKs')
        create_floatAttr(individual_object, 'Ik_Fk_Switch', 0, 10)
        create_boolAttr(individual_object, 'Indiv_Ctrls')
        create_floatAttr(individual_object, 'All_Curl', -10, 10)
        create_floatAttr(individual_object, 'All_Spread', -10, 10)

        create_curlAttrs(individual_object, big_curlAttrs)
        create_curlAttrs(individual_object, index_curlAttrs)
        create_curlAttrs(individual_object, mid_curlAttrs)
        create_curlAttrs(individual_object, fourth_curlAttrs)
        create_curlAttrs(individual_object, pinky_curlAttrs)

        create_spreadAttrs(individual_object, toe_spreadAttrs)


def add_handSwitchAttrs(*args):
    selection = cmds.ls(sl=True)

    for individual_object in selection:
        create_separatorAttr(individual_object, 'Hand_SDKs')
        create_floatAttr(individual_object, 'Ik_Fk_Switch', 0, 10)
        create_boolAttr(individual_object, 'Indiv_Ctrls')
        create_floatAttr(individual_object, 'All_Curl', -10, 10)
        create_floatAttr(individual_object, 'All_Spread', -10, 10)

        create_dropAttrs(individual_object, finger_dropAttrs)

        create_curlAttrs(individual_object, thumb_curlAttrs)
        create_curlAttrs(individual_object, index_curlAttrs)
        create_curlAttrs(individual_object, mid_curlAttrs)
        create_curlAttrs(individual_object, ring_curlAttrs)
        create_curlAttrs(individual_object, pinky_curlAttrs)

        create_spreadAttrs(individual_object, finger_spreadAttrs)


def create_dropAttrs(individual_object, attr_list):
    create_separatorAttr(individual_object, attr_list[0])
    create_floatAttr(individual_object, attr_list[1], -360, 360)
    create_floatAttr(individual_object, attr_list[2], -360, 360)


def create_curlAttrs(individual_object, attr_list):
    create_separatorAttr(individual_object, attr_list[0])
    create_floatAttr(individual_object, attr_list[1], -360, 360)
    create_floatAttr(individual_object, attr_list[2], -360, 360)
    create_floatAttr(individual_object, attr_list[3], -360, 360)


def create_spreadAttrs(individual_object, attr_list):
    create_separatorAttr(individual_object, attr_list[0])
    create_floatAttr(individual_object, attr_list[1], -360, 360)
    create_floatAttr(individual_object, attr_list[2], -360, 360)
    create_floatAttr(individual_object, attr_list[3], -360, 360)
    create_floatAttr(individual_object, attr_list[4], -360, 360)
    create_floatAttr(individual_object, attr_list[5], -360, 360)


def create_attr(*args):
    #old code :     attr_value = attributeType_radioGrp.getSelect()
    attr_value = cmds.radioButtonGrp(attributeType_radioGrp, q=True, sl=True)
    #Old codes : name = attribute_nameField.getText()
    name = cmds.textField(attribute_nameField, q=True, text=True)
    min_value = cmds.textField(attribute_minField, q=True, value=True)
    max_value = cmds.textField(attribute_maxField, q=True, value=True)

    selection = cmds.ls(sl=True)

    for individual_object in selection:
        if attr_value == 1:
            create_floatAttr(individual_object, name, min_value, max_value)

        elif attr_value == 2:
            create_intAttr(individual_object, name, min_value, max_value)

        elif attr_value == 3:
            create_boolAttr(individual_object, name)

        else:
            create_separatorAttr(individual_object, attr_name)

        print("Custom attribute '" + name + "' has been added to selected objects.")


def create_boolAttr(strCurrentControlCurveName, attr_name):
    cmds.addAttr(strCurrentControlCurveName, ln=attr_name, at='bool', dv=1, k=True)


def create_separatorAttr(strCurrentControlCurveName, attr_name):
    cmds.addAttr(strCurrentControlCurveName, ln=attr_name, at='enum', en='----------------')
    cmds.setAttr(strCurrentControlCurveName + '.' + attr_name, cb=True)


def create_floatAttr(strCurrentControlCurveName, attr_name, min_value, max_value):
    cmds.addAttr(strCurrentControlCurveName, ln=attr_name, at='double', min=min_value, max=max_value, k=True)


def create_intAttr(strCurrentControlCurveName, attr_name, min_value, max_value):
    cmds.addAttr(strCurrentControlCurveName, ln=attr_name, at='long', min=min_value, max=max_value, k=True)

# End Content of original file : rr_sub_curves_addAttributes.py



# Begin Content of original file : rr_sub_curves_lockHide.py

"""
RigBox Reborn - Sub: Lock and Hide Tool

Author: Jennifer Conley
Date Modified: 11/23/12

Description:
    A custom GUI to easily lock and hide unused transform channels of a control icon.
    
    Able to use preset options for FK and IK controls.

How to run:
    import rr_sub_curves_lockHide
    rr_sub_curves_lockHide.window_creation_LockHide()
"""

# Gui Creation
def window_creation_LockHide():
    if cmds.window(window_name_LockHide, q=True, ex=True):
        cmds.deleteUI(window_name_LockHide)
    if cmds.windowPref(window_name_LockHide, ex=True):
        cmds.windowPref(window_name_LockHide, r=True)

    window_object_LockHide = cmds.window(window_name_LockHide, bgc=window_bgc, w=width_ColorAttrLockHide, t='RigBox Reborn - Lock / Hide')
    gui_creation_LockHide()
    #Old code : window_object_LockHide.show()
    cmds.showWindow(window_object_LockHide)


def gui_creation_LockHide():
    global controlType_radioGrp
    global translate_checkBoxes, rotate_checkBoxes, scale_checkBoxes, visibility_checkBox

    main_col = cmds.columnLayout(w=width_ColorAttrLockHide, co=('both', 50))
    cmds.rowColumnLayout(nc=5, cw=[(1, 89), (2, cbw), (3, cbw), (4, cbw + 4), (5, cbw + 2)])
    cmds.text(l='', w=cbw)
    cmds.text(l='X', w=cbw)
    cmds.text(l='Y', w=cbw)
    cmds.text(l='Z', w=cbw)
    cmds.text(l='All', w=cbw)
    cmds.setParent(main_col)

    cmds.rowColumnLayout(nc=2, cw=[(1, 90), (2, 80)])
    cmds.text(l='Translation:')
    #Old code : translate_checkBoxes = cmds.checkBoxGrp('translate_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=cmds.Callback(set_checkBoxGrp, 'translate_checkBoxes'))
    translate_checkBoxes = cmds.checkBoxGrp('translate_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=partial(set_checkBoxGrp, 'translate_checkBoxes'))
    cmds.text(l='Rotation:')
    #Old code : rotate_checkBoxes = cmds.checkBoxGrp('rotate_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=cmds.Callback(set_checkBoxGrp, 'rotate_checkBoxes'))
    rotate_checkBoxes = cmds.checkBoxGrp('rotate_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=partial(set_checkBoxGrp, 'rotate_checkBoxes'))
    cmds.text(l='Scale: ')
    #Old code : scale_checkBoxes = cmds.checkBoxGrp('scale_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=cmds.Callback(set_checkBoxGrp, 'scale_checkBoxes'))
    scale_checkBoxes = cmds.checkBoxGrp('scale_checkBoxes', ncb=4, cw4=(cbw, cbw, cbw, cbw), cc4=partial(set_checkBoxGrp, 'scale_checkBoxes'))
    cmds.text(l='Visibility:')
    visibility_checkBox = cmds.checkBoxGrp('visibility_checkBox', cw=(1, cbw))
    cmds.setParent(main_col)

    cmds.separator(w=175, h=5)

    cmds.rowColumnLayout(nc=2, cw=[(1, 75), (2, 100)])
    #Old code : cmds.button(l='Lock / Hide', bgc=element_bgc, c=cmds.Callback(set_channels, 1))
    cmds.button(l='Lock / Hide', bgc=element_bgc, c=partial(set_channels, 1))
    #Old code : cmds.button(l='Show', bgc=element_bgc, c=cmds.Callback(set_channels, 0))
    cmds.button(l='Show', bgc=element_bgc, c=partial(set_channels, 0))
    cmds.setParent(main_col)

    cmds.separator(w=175, h=5)
    cmds.text(l='Selection Type', w=175)
    controlType_radioGrp = cmds.radioButtonGrp(la4=['Ik', 'Fk', 'All', 'None'], nrb=4, cw4=(40, 40, 40, 40), sl=4,
                                             cc=set_controlType)
    cmds.setParent(main_col)


# Work Fuctions
def get_checkBoxState(checkBox_list, checkBox_group):
    checkBox_list.append(cmds.checkBoxGrp(checkBox_group, q=True, v1=True))
    checkBox_list.append(cmds.checkBoxGrp(checkBox_group, q=True, v2=True))
    checkBox_list.append(cmds.checkBoxGrp(checkBox_group, q=True, v3=True))


def get_visibility():
    state = cmds.checkBoxGrp(visibility_checkBox, q=True, v1=True)

    return state


def set_ikControls():
    translate_checkBoxes.setValue4(False)
    rotate_checkBoxes.setValue4(True)
    scale_checkBoxes.setValue4(True)
    visibility_checkBox.setValue1(True)


def set_fkControls():
    translate_checkBoxes.setValue4(True)
    rotate_checkBoxes.setValue4(False)
    scale_checkBoxes.setValue4(True)
    visibility_checkBox.setValue1(True)


def set_allControls():
    translate_checkBoxes.setValue4(True)
    rotate_checkBoxes.setValue4(True)
    scale_checkBoxes.setValue4(True)
    visibility_checkBox.setValue1(True)


def set_noControls():
    translate_checkBoxes.setValue4(False)
    rotate_checkBoxes.setValue4(False)
    scale_checkBoxes.setValue4(False)
    visibility_checkBox.setValue1(False)


def set_controlType(*args):
    #old code :     ctrl_type = controlType_radioGrp.getSelect()
    ctrl_type = cmds.radioButtonGrp(controlType_radioGrp, q=True, sl=True)

    

    if ctrl_type == 1:
        set_ikControls()

    elif ctrl_type == 2:
        set_fkControls()

    elif ctrl_type == 3:
        set_allControls()

    elif ctrl_type == 4:
        set_noControls()

    set_checkBoxGrp('translate_checkBoxes')
    set_checkBoxGrp('rotate_checkBoxes')
    set_checkBoxGrp('scale_checkBoxes')


def set_checkBoxGrp(checkBox_group, *args):
    box_state = cmds.checkBoxGrp(checkBox_group, q=True, v4=True)

    if box_state:
        cmds.checkBoxGrp(checkBox_group, e=True, v1=True)
        cmds.checkBoxGrp(checkBox_group, e=True, v2=True)
        cmds.checkBoxGrp(checkBox_group, e=True, v3=True)

    else:
        cmds.checkBoxGrp(checkBox_group, e=True, v1=False)
        cmds.checkBoxGrp(checkBox_group, e=True, v2=False)
        cmds.checkBoxGrp(checkBox_group, e=True, v3=False)


def set_visibility(control_node, checkBox_state, lock):
    if checkBox_state:
        if lock:
            cmds.setAttr(control_node + '.v', l=True, k=False)
        else:
            cmds.setAttr(control_node + '.v', l=False, k=True)


def set_checkBox(control_node, attribute, checkBox_state, lock):
    if checkBox_state:
        if lock:
            cmds.setAttr(control_node + attribute, l=True, k=False)
        else:
            cmds.setAttr(control_node + attribute, l=False, k=True)


def set_channels(lock, *args):
    selection = cmds.ls(sl=True)

    checkBoxGrp_list = ['translate_checkBoxes', 'rotate_checkBoxes', 'scale_checkBoxes']
    checkBox_list = []
    attribute = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']

    vis_checkBox = get_visibility()

    for checkBox_group in checkBoxGrp_list:
        get_checkBoxState(checkBox_list, checkBox_group)

    for control_node in selection:
        set_visibility(control_node, vis_checkBox, lock)

        for i, checkBox in enumerate(checkBox_list):
            set_checkBox(control_node, attribute[i], checkBox, lock)

# End Content of original file : rr_sub_curves_lockHide.py



# Comment out following line when not testing!
window_creation_Main()