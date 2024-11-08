import argparse
import base64
import os
import re
import zlib
import json
import base64
import math

# Edit those values
TALISMANS_LEVEL = 250
EXP_INCREMENT_THRESHOLD = 6000000
EXP_INCREMENT_VALUE = 5500000
SHADOW_CORE_AMOUNT = 9999999999
SKILL_PTS_BOUGHT = 99465534
SKILLS_LEVELS = {
    'AMPLIFIERS': 1500,
    'ARMOR_TEARING': 1500,
    'BARRAGE': 50,
    'BEAM': 50,
    'BLEEDING': 1500,
    'BOLT': 50,
    'CRITHIT': 1500,
    'DEMOLITION': 50,
    'FREEZE': 50,
    'FURY': 50,
    'FUSION': 50,
    'ICESHARDS': 50,
    'LANTERNS': 50,
    'MANA_LEECHING': 1500,
    'MANA_STREAM': 50,
    'ORB_OF_PRESENCE': 50,
    'POISON': 1500,
    'PYLONS': 50,
    'RESONANCE': 1500,
    'SEEKER_SENSE': 50,
    'SLOWING': 1500,
    'TRAPS': 1200,
    'TRUE_COLORS': 1200,
    'UNKW1': -1,
    'UNKW2': -1,
    'WHITEOUT': 50,
}

BASE64CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

BATTLE_TRAITS = ['ADAPTIVE_CARAPACE', 'DARK_MASONRY', 'SWARMLING_DOMINATION', 'OVERCROWD', 'CORRUPTED_BANISHMENT', 'AWAKENING', 'INSULATION', 'HATRED', 'SWARMLING_PARASITES', 'HASTE', 'THICK_AIR', 'VITAL_LINK', 'GIANT_DOMINATION', 'STRENGTH_IN_NUMBERS', 'RITUAL']

TALISMAN_TYPES = ['EDGE', 'CORNER', 'INNER']

STAGES = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Y1', 'Y2', 'Y3', 'Y4', 'X1', 'X2', 'X3', 'X4', 'W1', 'W2', 'W3', 'W4', 'V1', 'V2', 'V3', 'V4', 'U1', 'U2', 'U3', 'U4', 'T1', 'T2', 'T3', 'T4', 'T5', 'S1', 'S2', 'S3', 'S4', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'O1', 'O2', 'O3', 'O4', 'N1', 'N2', 'N3', 'N4', 'N5', 'M1', 'M2', 'M3', 'M4', 'L1', 'L2', 'L3', 'L4', 'L5', 'K1', 'K2', 'K3', 'K4', 'K5', 'J1', 'J2', 'J3', 'J4', 'I1', 'I2', 'I3', 'I4', 'H1', 'H2', 'H3', 'H4', 'H5', 'G1', 'G2', 'G3', 'G4', 'F1', 'F2', 'F3', 'F4', 'F5', 'E1', 'E2', 'E3', 'E4', 'E5', 'D1', 'D2', 'D3', 'D4', 'D5', 'C1', 'C2', 'C3', 'C4', 'C5', 'B1', 'B2', 'B3', 'B4', 'B5', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']

SKILLS = ['MANA_STREAM', 'TRUE_COLORS', 'FUSION', 'ORB_OF_PRESENCE', 'RESONANCE', 'DEMOLITION', 'CRITHIT', 'MANA_LEECHING', 'BLEEDING', 'ARMOR_TEARING', 'POISON', 'SLOWING', 'FREEZE', 'WHITEOUT', 'ICESHARDS', 'BOLT', 'BEAM', 'BARRAGE', 'FURY', 'AMPLIFIERS', 'PYLONS', 'LANTERNS', 'TRAPS', 'SEEKER_SENSE', 'UNKW1', 'UNKW2']

STAT_DESCS = ["Battles won", " - Journey", " - Endurance", " - Trial", "Longest kill chain", "Waves started early", "Waves beaten", "Most waves beaten in one battle", "Walls built", "Towers built", "Traps built", "Amplifiers built", "Pylons built", "Lanterns built", "Mana spent on gems", " - Mana leeching", " - Critical hit", " - Poison", " - Bleeding", " - Slowing", " - Armor tearing", "Highest grade gem created", "Highest gem maximum damage reached", "Highest mana reached", "Highest mana pool level reached", "Mana harvested from regular mana shards", "Mana harvested from corrupted mana shards", "Swarmlings lured in by enraging waves", "Reavers lured in by enraging waves", "Giants lured in by enraging waves", "Swarmlings lured out of sleeping hives", "Swarmlings killed", "Reavers killed", "Giants killed", "Apparitions killed", "Specters killed", "Spires killed", "Shadows killed", "Guardians killed", "Wraiths killed", "Wizard hunters killed", "Wallbreakers killed", "Swarm queens killed", "Marked monsters killed", "Twisted monsters killed", "Possessed monsters killed", "Tombs raided", "Beacons destroyed", "Barricades destroyed", "Monster nests destroyed", "Drop holders opened", "Houses destroyed", "Jars of wasps broken", "Monster eggs cracked", "Watchtowers destroyed", "Mana shards depleted", "Tower shot kills", "Trap kills", "Pylon kills", "Lantern kills", "Gem bomb kills", "Gem wasp kills", "Bolt kills", "Beam kills", "Barrage shell kills", "Poison kills", "Shrine kills", "Ice shard kills", "Whited out orb kills", "Frozen explosion kills", "One hit kills", "Freeze spells cast", "Whiteout spells cast", "Ice shards spells cast", "Bolt spells cast", "Beam spells cast", "Barrage spells cast", "Freeze spells total hits", "Whiteout spells total hits", "Ice shards spells total hits", "Talisman fragments found", "Shrines activated", "Gem bombs thrown", "Demolitions used", "Banishments done by the Orb", "Exploding orblet kills"]

COMPRESSED_STRS = [" ", "!", "#", "$", "%", "&", "(", ")", "*", ".", ":", ";", "<", ">", "@", "[", "]", "_", "{", "|", "}"]

UNCOMPRESSED_STRS = [",B", ",C", ",D", ",E", ",F", ",G", ",H", ",I", ",J", ",K", ",L", ",M", ",N", ",O", ",P", ",Q", ",R", ",S", ",T", ",U", ",V"]

CHECKSUM_LENGTH = 16

def deep_merge(dict1, dict2):
    """
    Recursively merges two dicts, combining nested dics and lists.
    """
    output = dict(dict1)
    for key, value in dict2.items():
        if key in output:
            if isinstance(value, dict) and isinstance(output[key], dict):
                output[key] = deep_merge(output[key], value)
            elif isinstance(value, list) and isinstance(output[key], list):
                # Fuse listes without duplicates
                output[key] = output[key] + [item for item in value if item not in output[key]]
            else:
                output[key] = value
        else:
            output[key] = value
    return output

def decode_expr(vDataArr):
    stageHighestXpsJourney = []
    stageHighestXpsEndurance = []
    stageHighestXpsTrial = []

    iLim = len(vDataArr) // 3
    
    for i in range(iLim):
        vXpStr = vDataArr.pop(0)
        stageHighestXpsJourney.append(base64_to_base10(vXpStr))
        
        vXpStr = vDataArr.pop(0)
        stageHighestXpsEndurance.append(base64_to_base10(vXpStr))
        
        vXpStr = vDataArr.pop(0)
        stageHighestXpsTrial.append(base64_to_base10(vXpStr))

    return {
        'stageHighestXpsJourney': dict(zip(STAGES, stageHighestXpsJourney)),
        'stageHighestXpsEndurance': dict(zip(STAGES, stageHighestXpsEndurance)),
        'stageHighestXpsTrial': dict(zip(STAGES, stageHighestXpsTrial)),
    }

def encode_expr(expr_data: dict) -> list:
    """
    Encodes experience data from a dictionary format into a Base64-encoded list for use in vDataArr.

    Args:
        expr_data (dict): A dictionary with keys 'stageHighestXpsJourney', 'stageHighestXpsEndurance',
                          and 'stageHighestXpsTrial', each containing a dictionary of experience points
                          for each stage.

    Returns:
        list: A list of Base64-encoded strings representing the encoded experience data.
    """
    vDataArr = []

    # Encode the experience points for each stage in the correct order
    for stage in STAGES:
        journey_xp = expr_data['stageHighestXpsJourney'].get(stage, 0)
        endurance_xp = expr_data['stageHighestXpsEndurance'].get(stage, 0)
        trial_xp = expr_data['stageHighestXpsTrial'].get(stage, 0)
        
        # Convert each experience point to Base64 and add to vDataArr
        vDataArr.append(base10_to_base64(journey_xp))
        vDataArr.append(base10_to_base64(endurance_xp))
        vDataArr.append(base10_to_base64(trial_xp))

    return vDataArr

def decode_talismans(vDataArr):
    talismanInventory = []
    iLim = len(vDataArr)
    for i in range(iLim):
        talismanData = vDataArr[i]
        if talismanData == '-1':
            talismanInventory.append(None)
        else:
            byte_data = base64_decode_byte_array(talismanData)
            decoded_string = byte_data.decode('utf-8')
            arrData = decoded_string.split("/")

            talisman = {
                'seed': int(arrData[0]),
                'rarity': int(arrData[1]),
                'type': int(arrData[2]),
                'typeName': TALISMAN_TYPES[int(arrData[2])],
                'upgradeLevel': int(arrData[3]),
                'linkUp': int(arrData[4]),
                'linkRight': int(arrData[5]),
                'linkDown': int(arrData[6]),
                'linkLeft': int(arrData[7]),
            }

            talismanInventory.append(talisman)
    
    return talismanInventory

def encode_talismans(talismanInventory: list) -> list:
    """
    Encodes a list of talisman dictionaries into a Base64-encoded list for use in vDataArr.

    Args:
        talismanInventory (list): A list of dictionaries representing talismans. Each dictionary contains
                                  keys such as 'seed', 'rarity', 'type', 'upgradeLevel', 'linkUp', 
                                  'linkRight', 'linkDown', and 'linkLeft'.

    Returns:
        list: A list of strings where each string is a Base64-encoded talisman, or '-1' for None entries.
    """
    vDataArr = []

    for talisman in talismanInventory:
        if talisman is None:
            # Represent empty talismans with '-1'
            vDataArr.append('-1')
        else:
            # Create the encoded string using the talisman fields
            talisman_str = f"{talisman['seed']}/{talisman['rarity']}/{talisman['type']}/" \
                           f"{talisman['upgradeLevel']}/{talisman['linkUp']}/" \
                           f"{talisman['linkRight']}/{talisman['linkDown']}/{talisman['linkLeft']}"
            
            # Convert to bytes, then Base64-encode
            talisman_bytes = talisman_str.encode('utf-8')
            encoded_data = base64_encode_byte_array(talisman_bytes)
            vDataArr.append(encoded_data)

    return vDataArr


def handle_xpmu2(vDataArr):
    journeyXpRecXpMults = []
    enduranceXpRecXpMults = []
    trialXpRecXpMults = []

    iLim = len(vDataArr) // 3
    
    for i in range(iLim):
        journeyXpRecXpMults.append(float(vDataArr.pop(0)) / 100)
        enduranceXpRecXpMults.append(float(vDataArr.pop(0)) / 100)
        trialXpRecXpMults.append(float(vDataArr.pop(0)) / 100)

    return {
        'journeyXpRecXpMults': dict(zip(STAGES, journeyXpRecXpMults)),
        'enduranceXpRecXpMults': dict(zip(STAGES, enduranceXpRecXpMults)),
        'trialXpRecXpMults': dict(zip(STAGES, trialXpRecXpMults)),
    }

def extract_data_segments(encoded_str: str) -> dict:
    # Replace compressed strings with uncompressed equivalents
    decoded_str = encoded_str[:]
    for compressed, uncompressed in zip(COMPRESSED_STRS, UNCOMPRESSED_STRS):
        while compressed in decoded_str:
            decoded_str = decoded_str.replace(compressed, uncompressed)

    # Split the decoded string into an array of data segments
    return decoded_str.split(",?,")

def combine_data_segments(data_segments: list) -> str:
    """
    Combines a list of data segments into a single encoded string, applying compression.

    Args:
        data_segments (list): A list of strings where each string is a data segment.

    Returns:
        str: The combined, encoded string with compression applied.
    """
    # Combine all data segments with ",?," separator
    combined_str = ",?,".join(data_segments)

    # Replace uncompressed strings with compressed equivalents
    for uncompressed, compressed in zip(UNCOMPRESSED_STRS, COMPRESSED_STRS):
        while uncompressed in combined_str:
            combined_str = combined_str.replace(uncompressed, compressed)

    return combined_str


def data_to_json(encoded_str: str) -> dict:
    """
    Parses an encoded string into a dictionary of player data, replacing compressed strings 
    and interpreting various data tags to construct the player’s game state.

    Args:
        encoded_str (str): The compressed and encoded input string containing player data.

    Returns:
        dict: A dictionary representing the decoded player data.
    """
    # Initialize dictionary to store player data
    player_data = {
        "ppdVersion": None,
        "recoveredEnduranceXpMult": None,
        "recoveredEnduranceXp": None,
        "recoveredEnduranceWavesBeaten": None,
        "recoveredEnduranceTraitSet": [], # [0] * 15,
        "recoveredEnduranceFieldStrId": None,
        "recoveredEnduranceTalFragsBase64": None,
        "achiResetSkillPtBonus": None,
        "selectedSkillLevels": [],
        "stats": [],
        "gainedAchis": [],
        "gainedTutorialPages": [],
        "gainedJourneyPages": [],
        "stageHighestXpsJourney": [],
        "stageHighestXpsEndurance": [],
        "stageHighestXpsTrial": [],
        "enduranceXpRecWavesBeaten": [],
        "gainedSkillTomes": [],
        "gainedBattleTraits": [],
        "stageWizStashStauses": [],
        "stageAlloyStashStauses": [],
        "enduranceXpRecTraitSets": [],
        "journeyXpRecTraitSets": [],
        "journeyXpRecXpMults": [],
        "enduranceXpRecXpMults": [],
        "trialXpRecXpMults": [],
        "gainedMapTiles": [],
        "selectedBattleTraitLevels": [],
        "talismanInventory": [],
        "talismanSlots": [],
        "talSlotUnlockStatuses": [],
        "talFragShapeCollection": [],
        "skillPtsBought": None,
        "skillPtsFromLoot": None,
        "gainedEnduranceWaveStones": None,
        "shadowCoreAmount": None,
        "talFragRarityBoostsLeft": None,
        "gameMode": None,
        "modKeysSeed": None,
        "modUnlockStatuses": [],
        "modActivationStatuses": []
    }

    data_segments = extract_data_segments(encoded_str)

    # Process each segment based on the tag and populate the player data dictionary
    for segment in data_segments:
        segment_parts = segment.split(",")
        tag = segment_parts.pop(0)
        
        if tag == "VERS":
            player_data["ppdVersion"] = segment_parts[0]
        elif tag == "REXM":
            player_data["recoveredEnduranceXpMult"] = float(segment_parts[0])
        elif tag == "REXP":
            player_data["recoveredEnduranceXp"] = float(segment_parts[0])
        elif tag == "REXW":
            player_data["recoveredEnduranceWavesBeaten"] = int(segment_parts[0])
        elif tag == "REXT":
            player_data["recoveredEnduranceTraitSet"][:len(segment_parts)] = segment_parts
        elif tag == "REID":
            player_data["recoveredEnduranceFieldStrId"] = segment_parts[0]
        elif tag == "RETF":
            player_data["recoveredEnduranceTalFragsBase64"] = segment_parts[0]
        elif tag == "ARBN":
            player_data["achiResetSkillPtBonus"] = int(segment_parts[0])
        elif tag == "SKLV":
            skill_levels = [base64_to_base10(level) for level in segment_parts]
            player_data["selectedSkillLevels"] = dict(zip(SKILLS, skill_levels))
        elif tag == "STAT":
            stats = [base64_to_base10(stat) for stat in segment_parts]
            player_data["stats"] = dict(zip(STAT_DESCS, stats))
        elif tag == "ACHI":
            player_data["gainedAchis"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "TUTP":
            player_data["gainedTutorialPages"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "JRNP":
            player_data["gainedJourneyPages"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "EXPR":
            player_data.update(decode_expr(segment_parts))
        elif tag == "ENRW":
            player_data["enduranceXpRecWavesBeaten"] = dict(zip(STAGES, segment_parts))
        elif tag == "SKTM":
            player_data["gainedSkillTomes"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "BTLG":
            player_data["gainedBattleTraits"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "WSST":
            # TODO: Complex logic for gainedBattleTraits and gainedSkillTomes with StashDrops
            pass
        elif tag == "ASST":
            # TODO: Complex logic for gainedSkillTomes with AlloyStashStatuses
            pass
        elif tag == "ENRT":
            # TODO: Handle nested trait sets for enduranceXpRecTraitSets
            pass
        elif tag == "JRRT":
            # TODO: Handle nested trait sets for journeyXpRecTraitSets
            pass
        elif tag == "XPMU2":
            player_data.update(handle_xpmu2(segment_parts))
        elif tag == "MAPT":
            player_data["gainedMapTiles"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "BTLS":
            battle_trait_levels = [base64_to_base10(level) for level in segment_parts]
            player_data["selectedBattleTraitLevels"] = dict(zip(BATTLE_TRAITS, battle_trait_levels))
        elif tag == "TALI":
            player_data["talismanInventory"] = decode_talismans(segment_parts)
        elif tag == "TALA":
            player_data["talismanSlots"] = decode_talismans(segment_parts)
        elif tag == "TALF":
            player_data["talSlotUnlockStatuses"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "TALS":
            player_data["talFragShapeCollection"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "SKPB":
            player_data["skillPtsBought"] = int(segment_parts[0])
        elif tag == "SKLT":
            player_data["skillPtsFromLoot"] = int(segment_parts[0])
        elif tag == "ENDW":
            player_data["gainedEnduranceWaveStones"] = round(float(segment_parts[0]))
        elif tag == "SHCR":
            player_data["shadowCoreAmount"] = int(segment_parts[0])
        elif tag == "RARB":
            player_data["talFragRarityBoostsLeft"] = int(segment_parts[0])
        elif tag == "GMOD":
            player_data["gameMode"] = int(segment_parts[0])
        elif tag == "MODK":
            player_data["modKeysSeed"] = int(segment_parts[0])
        elif tag == "MODS":
            player_data["modUnlockStatuses"] = get_value_from_bitarray(segment_parts[0])
        elif tag == "MODA":
            player_data["modActivationStatuses"] = get_value_from_bitarray(segment_parts[0])

    return player_data

def alter_data(encoded_str: str, alteration_data: dict) -> str:
    """
    Converts player data from a dictionary format back to a compressed string format.
    This initial implementation only supports the EXPR, TALI, and TALA fields.

    Args:
        player_data (dict): The player data dictionary.

    Returns:
        str: The compressed, encoded string representation of the player data.
    """
    data_segments = extract_data_segments(encoded_str)

    player_data = data_to_json(encoded_str)
    # print(json.dumps(player_data, indent=2))

    altered_data = deep_merge(player_data, alteration_data)

    for i, line in enumerate(data_segments):
        if line.startswith('EXPR'):
            # Handle the EXPR field (experience points across different modes)
            if 'stageHighestXpsJourney' in altered_data and 'stageHighestXpsEndurance' in altered_data and 'stageHighestXpsTrial' in altered_data:
                for j, exp in altered_data['stageHighestXpsJourney'].items():
                    if 0 < exp and exp < EXP_INCREMENT_THRESHOLD:
                        exp += EXP_INCREMENT_VALUE

                    altered_data['stageHighestXpsJourney'][j] = exp

                for j, exp in altered_data['stageHighestXpsEndurance'].items():
                    if 0 < exp and exp < EXP_INCREMENT_THRESHOLD:
                        exp += EXP_INCREMENT_VALUE

                    altered_data['stageHighestXpsEndurance'][j] = exp

                expr_segment = "EXPR"
                expr_segment += ',' + ','.join(encode_expr(altered_data))
                data_segments[i] = expr_segment

        if line.startswith('TALI'):
            # Handle the TALI field (talisman inventory)
            if 'talismanInventory' in altered_data:
                for j, talisman in enumerate(altered_data['talismanInventory']):
                    if talisman is None:
                        continue
                                        
                    if talisman['rarity'] < TALISMANS_LEVEL:
                        talisman['rarity'] = TALISMANS_LEVEL

                    altered_data['talismanInventory'][j] = talisman

                tali_segment = "TALI"
                tali_segment += ',' + ','.join(encode_talismans(altered_data['talismanInventory']))

                data_segments[i] = tali_segment

        if line.startswith('TALA'):
            # Handle the TALA field (talisman slots)
            if 'talismanSlots' in altered_data:
                for j, talisman in enumerate(altered_data['talismanSlots']):
                    if talisman is None:
                        continue
                                        
                    if talisman['rarity'] < TALISMANS_LEVEL:
                        talisman['rarity'] = TALISMANS_LEVEL

                    altered_data['talismanSlots'][j] = talisman

                tali_segment = "TALA"
                tali_segment += ',' + ','.join(encode_talismans(altered_data['talismanSlots']))

                data_segments[i] = tali_segment

        if line.startswith('SKPB'):
            # Handle the SKPB field (skill points bought)
            if 'skillPtsBought' in altered_data:
                skpb_segment = "SKPB"
                skpb_segment += ',' + str(altered_data['skillPtsBought'])

                data_segments[i] = skpb_segment

        if line.startswith('SKLV'):
            # Handle the SHCR field (shadow cores)
            if 'selectedSkillLevels' in altered_data:
                sklv_segment = "SKLV"
                for skill_key, skill_level in altered_data['selectedSkillLevels'].items():
                    if skill_key in SKILLS_LEVELS:
                        new_level = SKILLS_LEVELS[skill_key]
                    else:
                        new_level = skill_level

                    skill_level_b64 = base10_to_base64(new_level)

                    sklv_segment += ',' + str(skill_level_b64)

                data_segments[i] = sklv_segment

    return combine_data_segments(data_segments)


def get_value_from_bitarray(base64_str):
    """
    Decodes a base64-encoded string into a list of boolean values representing individual bits.

    Args:
        base64_str (str): A base64-encoded string.

    Returns:
        list: A list of boolean values where each value corresponds to a bit in the decoded binary data.
    """
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    bit_values = []
    
    # Calculate the total number of bits to be read from the base64 string
    total_bits = len(base64_str) * 6
    
    def read_bit(encoded_str, bit_position):
        """
        Reads a specific bit from the base64-encoded string.

        Args:
            encoded_str (str): The base64 string.
            bit_position (int): Position of the bit to be read.

        Returns:
            bool: True if the bit is '1', otherwise False.
        """
        # Determine the character and convert it to a 6-bit binary string
        char_index = math.floor((bit_position + 0.0001) / 6)
        char_value = BASE64_CHARS.index(encoded_str[char_index])
        
        # Convert character to binary and pad to 6 bits
        binary_str = bin(char_value)[2:].zfill(6)
        
        # Return True if the specified bit is '1', otherwise False
        return binary_str[bit_position % 6] == "1"

    # Iterate over the total number of bits and retrieve each bit as a boolean
    for i in range(total_bits):
        bit_values.append(read_bit(base64_str, i))

    return bit_values


def base64_decode_byte_array(encoded_data: str) -> bytes:
    """
    Decodes a base64-encoded string into a byte array.

    Args:
        encoded_data (str): Base64 encoded string.

    Returns:
        bytes: Decoded byte array.
    """
    # Initialize buffers and the result byte array
    data_buffer = [0] * 4
    output_buffer = [0] * 3
    decoded_bytes = bytearray()
    
    # Process each 4-character group in the base64 string
    index = 0
    while index < len(encoded_data):
        # Fill data_buffer with base64 indices, using 64 as padding if needed
        for j in range(4):
            if index + j < len(encoded_data):
                data_buffer[j] = BASE64CHARS.index(encoded_data[index + j])
            else:
                data_buffer[j] = 64  # Padding indicator for base64

        # Convert data_buffer values to bytes and store in output_buffer
        output_buffer[0] = (data_buffer[0] << 2) + ((data_buffer[1] & 0x30) >> 4)
        output_buffer[1] = ((data_buffer[1] & 0x0F) << 4) + ((data_buffer[2] & 0x3C) >> 2)
        output_buffer[2] = ((data_buffer[2] & 0x03) << 6) + data_buffer[3]

        # Append decoded bytes to the result until padding is encountered
        for byte in output_buffer:
            if data_buffer[output_buffer.index(byte) + 1] == 64:  # Check for padding
                break
            decoded_bytes.append(byte)
        
        # Move to the next 4-character group
        index += 4

    return bytes(decoded_bytes)

def base64_encode_byte_array(byte_data: bytes) -> str:
    """
    Encodes a byte array into a base64-encoded string.

    Args:
        byte_data (bytes): The byte array to encode.

    Returns:
        str: The base64 encoded string.
    """
    BASE64CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # Initialize encoded string result
    encoded_str = ""
    data_buffer = [0] * 3  # Buffer for holding 3 bytes
    output_buffer = [0] * 4  # Buffer for holding 4 base64 indices
    
    # Process each 3-byte group in the byte_data
    index = 0
    while index < len(byte_data):
        # Fill the data buffer with up to 3 bytes, padding with 0 if needed
        for i in range(3):
            if index + i < len(byte_data):
                data_buffer[i] = byte_data[index + i]
            else:
                data_buffer[i] = 0  # Padding for remaining buffer spaces
        
        # Map the 3 bytes in data_buffer to 4 base64 characters in output_buffer
        output_buffer[0] = (data_buffer[0] >> 2) & 0x3F
        output_buffer[1] = ((data_buffer[0] & 0x03) << 4) | ((data_buffer[1] >> 4) & 0x0F)
        output_buffer[2] = ((data_buffer[1] & 0x0F) << 2) | ((data_buffer[2] >> 6) & 0x03)
        output_buffer[3] = data_buffer[2] & 0x3F
        
        # Append base64 characters to the result string
        for j in range(4):
            if index + j < len(byte_data) + 1 or j < 2:
                encoded_str += BASE64CHARS[output_buffer[j]]
            else:
                encoded_str += "="  # Add padding '=' for incomplete 3-byte groups

        # Move to the next 3-byte group
        index += 3

    return encoded_str


def base10_to_base64(value: int) -> str:
    """
    Converts a base-10 integer into a base64-encoded string.

    Args:
        value (int): The base-10 integer to convert.

    Returns:
        str: The base64-encoded string representation of the input integer.
    """
    is_negative = value < 0
    value = abs(round(value))
    result = ""
    exponent = 0
    
    while value > 0:
        current_value_to_base64_digit = value % (64 ** (exponent + 1))
        value -= current_value_to_base64_digit
        current_value_to_base64_digit = round(current_value_to_base64_digit / (64 ** exponent))
        result = BASE64CHARS[int(current_value_to_base64_digit)] + result
        exponent += 1
    
    if is_negative:
        result = "-" + result
    
    return result


def base64_to_base10(base64_str: str) -> int:
    """
    Converts a base64-encoded string into a base-10 integer.

    Args:
        base64_str (str): A base64-encoded string representing a number.

    Returns:
        int: The base-10 integer representation of the base64-encoded input.
    """
    is_negative = base64_str.startswith("-")
    if is_negative:
        base64_str = base64_str[1:]
    
    base10_value = 0
    length = len(base64_str)
    
    for i in range(length):
        base10_value += BASE64CHARS.index(base64_str[i]) * (64 ** (length - i - 1))
    
    if is_negative:
        base10_value *= -1
    
    return base10_value

def calculate_checksum(input_str: str) -> str:
    """
    Calculates a checksum for a given string by calling `calculate_checksum_step` 
    twice, with steps 0 and 1, and concatenating the results.

    Args:
        input_str (str): The input string for which to calculate the checksum.

    Returns:
        str: The concatenated checksum as a string.
    """

    return str(calculate_checksum_step(input_str, 0)) + str(calculate_checksum_step(input_str, 1))

def calculate_checksum_step(input_str: str, step: int) -> str:
    """
    Calculates the checksum for a specific step.

    Args:
        input_str (str): The string for which the checksum is calculated.
        step (int): Step parameter (0 or 1) to select calculation constants.

    Returns:
        str: The checksum for the specified step, represented as a string.
    """
    # Define constants based on the step
    checksum = [72348482, 31264582][step]
    shifter_base = [27931, 90542][step]
    modulo_base = [94382618, 90542157][step]
    bloater = [76, 122][step]
    
    # Calculate checksum by iterating over the input string
    for index, char in enumerate(input_str):
        checksum = (
            checksum * (ord(char) + bloater + index * 111) % (modulo_base - 105) 
            + shifter_base - 5
        )
    
    # Ensure checksum is within specified range and return as string
    checksum = checksum % 89999999 + 10000000

    return str(round(abs(checksum)))


def alter_save(file):
    base_path = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    extracted_save_path = f"{base_path}.extracted{extension}"
    extracted_json_save_path = f"{base_path}.extracted.json"
    altered_save_path = f"{base_path}.altered{extension}"

    with open(file, 'r') as file:
        data_and_checksum = file.read()

    checksum = data_and_checksum[-CHECKSUM_LENGTH:]
    data = data_and_checksum[0:-CHECKSUM_LENGTH]

    try:
        decoded_data = base64.b64decode(data)
    except Exception as e:
        print(f"Error during decoding data: {e}")
        return

    try:
        decompressed_data = zlib.decompress(decoded_data)
    except Exception as e:
        print(f"Error during decompressing data: {e}")
        return

    with open(extracted_save_path, 'wb') as exported_save_file:
        exported_save_file.write(decompressed_data)

    decoded_data = decompressed_data.decode('utf-8')

    extracted_json = data_to_json(decoded_data)

    with open(extracted_json_save_path, 'w') as extracted_json_save_file:
        extracted_json_save_file.write(json.dumps(extracted_json, indent=2))
        print(f'Data extracted to {extracted_json_save_path}')

    # New alter data
    alteration_data = {
        'shadowCoreAmount': SHADOW_CORE_AMOUNT,
        'skillPtsBought': SKILL_PTS_BOUGHT,
    }
    altered_str = alter_data(decoded_data, alteration_data)

    # Compress data
    compressor = zlib.compressobj(
        level=9,
        method=zlib.DEFLATED,
        wbits=15,
        memLevel=5,
        strategy=0
    )

    compressed_data = compressor.compress(altered_str.encode('utf-8'))
    compressed_data += compressor.flush()

    altered_data = base64.b64encode(compressed_data)

    new_checksum = calculate_checksum(altered_data.decode('utf-8'))

    altered_data_with_checksum = altered_data + new_checksum.encode('utf-8')

    with open(altered_save_path, 'wb') as exported_save_file:
        exported_save_file.write(altered_data_with_checksum)
        print(f'Altered savefile saved to {altered_save_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='GemCraft Frostborn Wrath Save Editor'
    )
    parser.add_argument('source_savefile_path') 
    args = parser.parse_args()

    if not os.path.exists(args.source_savefile_path):
        raise FileNotFoundError(f"The file {args.source_savefile_path} does not exist.")

    alter_save(args.source_savefile_path)
