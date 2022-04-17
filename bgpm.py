#!/usr/bin/env python3

import pybgpstream
"""Code file for CS 6250 BGPM Project

Edit this file according to the provided docstrings and assignment description. 
Do not change the existing function name or arguments.
You may add additional functions but they need to be contained entirely in this file.
"""

def calculateUniquePrefixes(cache_files):
    """Retrieve the number of unique IP prefixes from input BGP data files.

    Args:
        cache_files: A list of files.

    Returns:
        A list containing the number of unique IP prefixes for each input file.
        For example: [2, 5]
    """
    _cache_files = sorted(cache_files)

    ip_list = []
    for f in _cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
        stream.stream.set_data_interface_option("singlefile", "rib-file", f)
        prefixes = set()
        for elem in stream:
            p = elem._maybe_field("prefix")
            prefixes.add(p)

        ip_list.append(len(prefixes))

    return ip_list


def calculateUniqueAses(cache_files):
    """Retrieve the number of unique ASes from input BGP data files.

    Args:
        cache_files: A list of files.

    Returns:
        A list containing the number of the number of unique AS for each input file.
        For example: [2, 5]
    """
    _cache_files = sorted(cache_files)

    as_list = []
    for f in _cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
        stream.stream.set_data_interface_option("singlefile", "rib-file", f)
        ases = set()
        for elem in stream:
            _ases = elem._maybe_field("as-path")
            for _as in _ases.split(" "):
                if _as != "":
                    ases.add(_as)

        as_list.append(len(ases))

    return as_list


def examinePrefixes(cache_files):
    """A list of the top 10 origin ASes according to percentage increase of the advertised prefixes.

    Args:
        cache_files: A list of files.

    Returns:
        A list of the top 10 origin ASes according to percentage increase of the advertised prefixes from lowest to highest.
        For example: ["777", "1", "6"]
        corresponds to AS "777" as having the smallest percentage increase (of the top ten) and AS "6" having the highest increase (of the top ten).
        AS numbers should be strings.
    """
    _cache_files = sorted(cache_files)

    as_origins = dict()  # keys: as, num_of_first, set
    for f in _cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
        stream.stream.set_data_interface_option("singlefile", "rib-file", f)

        for elem in stream:
            origin = elem._maybe_field("as-path").split(" ")[-1]
            p = elem._maybe_field("prefix")

            if origin in as_origins.keys():
                if f in as_origins[origin].keys():
                    as_origins[origin][f].add(p)
                else:
                    as_origins[origin][f] = {p}
            else:
                # it is not recorded, this is the first time we have seen this origin
                as_origins[origin] = {f: {p}}

    pct_increase = dict()
    for origin in as_origins.keys():
        origin_dict = as_origins[origin]
        if len(origin_dict.keys()) == 1:  # only showed up in one snapshot
            pct_increase[origin] = 1
        else:
            try:
                origin_dict_keys = list(origin_dict.keys())
                pct_increase[origin] = len(origin_dict[origin_dict_keys[-1]]) / len(origin_dict[origin_dict_keys[0]])
            except TypeError:
                import pdb; pdb.set_trace()

    ranked_list = sorted(pct_increase.items(), key=lambda x:x[1])
    top_ten = []
    for _as in ranked_list[-10:]:
        top_ten.append(_as[0])

    top_ten.reverse()
    return top_ten


def calculateShortestPath(cache_files):
    """Compute the shortest AS path length for every origin AS from input BGP data files.

    Retrieves the shortest AS path length for every origin AS for every input file.
    Your code should return a dictionary where every key is the AS string and every value associated with the key is
    a list of the shortest path lengths for that AS.

    Note: For any AS that is not present in every input file, fill the corresponding entry in its list with a zero.
    Every value in the dictionary should have the same length.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where every key is the AS and every value associated with the key is a list of the shortest path
        lengths for that AS, for every input file.
        For example: {"455": [4, 2, 3], "533": [4, 1, 2]}
        corresponds to the AS "455" with the shortest path lengths 4, 2 and 3 and the AS "533" with the shortest paths 4, 1 and 2.
        AS numbers should be strings.
    """
    _cache_files = sorted(cache_files)
    count_list_template = []
    for i in range(len(_cache_files)):
        count_list_template.append(0)
        # make a template like [0, 0, 0, 0, 0, 0, 0]

    as_list = dict()
    for idx, f in enumerate(_cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
        stream.stream.set_data_interface_option("singlefile", "rib-file", f)

        for elem in stream:
            _ases = elem._maybe_field("as-path")
            if _ases == '':
                continue
            as_path = _ases.split(" ")
            _as_path = [i for i in as_path if i != '']
            origin_as = _as_path[-1]

            count = get_count_of_unique_as_path(as_path)  # list of unique as_path
            if count == 1:
                continue  # filter out all paths of 1

            if origin_as in as_list.keys():
                if as_list[origin_as][idx] == 0 or count < as_list[origin_as][idx]:
                    as_list[origin_as][idx] = count
            else:
                # add origin to
                as_list[origin_as] = count_list_template.copy()
                as_list[origin_as][idx] = count

    return as_list


def get_count_of_unique_as_path(as_list):
    u_as_list = set(as_list)  # unique list, takes care of duplicates
    u_as_list.remove(' ') if ' ' in u_as_list else 0
    u_as_list.remove('') if '' in u_as_list else 0
    return len(u_as_list)


def calculateRTBHDurations(cache_files):
    """Identify blackholing events and compute the duration of all RTBH events from input BGP data files.

    Identify events where the IPV4 prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a prefix and each
        value equal to a list of explicit RTBH event durations.
        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
        AS numbers should be strings.
    """
    _cache_files = sorted(cache_files)

    peer_ips = get_peer_ips(_cache_files)
    result = dict()

    state = dict()  # prefix, community
    for peer_ip in peer_ips:
        state[peer_ip] = dict()

        for f in _cache_files:
            stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
            stream.stream.set_data_interface_option("singlefile", "upd-file", f)

            for elem in stream:
                if elem.peer_address == peer_ip:
                    prefix = elem.fields['prefix']
                    if elem.type == 'A':
                        communities = elem._maybe_field("communities")
                        rtbh_tokens = get_rtbh_tokens(communities)
                        if len(rtbh_tokens) > 0:
                            # for each blackholed community, track time
                            for rtbh_token in rtbh_tokens:

                                if prefix not in state[peer_ip].keys():
                                    state[peer_ip][prefix] = dict()

                                state[peer_ip][prefix][rtbh_token] = elem.time
                        else:
                            # Filter out implicit withdrawals
                            if prefix in state[peer_ip].keys():
                                state[peer_ip].pop(prefix, None)

                    elif elem.type == 'W':
                        if prefix in state[peer_ip].keys():
                            # iterate over each comm string and calculate time
                            for rtbh_token in state[peer_ip][prefix].keys():
                                time_passed = elem.time - state[peer_ip][prefix][rtbh_token]
                                if time_passed > 0:
                                    # filter out those with time 0
                                    add_to_task3_result(peer_ip, prefix, time_passed, result)
                            state[peer_ip].pop(prefix, None)

        if len(state[peer_ip]) == 0:
            state.pop(peer_ip)

    return result


def add_to_task3_result(peer_ip, prefix, time_passed, result):
    if peer_ip not in result.keys():
        result[peer_ip] = dict()

    if prefix not in result[peer_ip].keys():
        result[peer_ip][prefix] = []

    result[peer_ip][prefix].append(time_passed)


def get_rtbh_tokens(comm_set):
    rtbh_tokens = []
    for t in comm_set:
        rtbh_tokens.append(t) if '666' in t else 0

    return rtbh_tokens


def get_peer_ips(source_files):
    peer_ips = set()

    for f in source_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
        stream.stream.set_data_interface_option("singlefile", "upd-file", f)

        for elem in stream:
            comm = elem._maybe_field("communities")
            peer_ips.add(elem.peer_address) if elem.peer_address != '' else 'bogus'

    return peer_ips


def calculateAWDurations(cache_files):
    """Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input data.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a prefix and each
        value equal to a list of explicit AW event durations.
        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
        AS numbers should be strings.
    """
    _cache_files = sorted(cache_files)
    # for Debug
    # for f in _cache_files:
    #     stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
    #     stream.stream.set_data_interface_option("singlefile", "upd-file", f)
    #
    #     for elem in stream:
    #         if elem.type == 'A' and elem.fields['prefix'] == '99.194.200.0/22':
    #             comm = elem._maybe_field("communities")
    #             if '666' in elem._maybe_field("communities"):
    #                 print(elem._maybe_field("communities"))
    # return {}

    peer_ips = get_peer_ips(_cache_files)
    result = dict()

    state = dict()
    for peer_ip in peer_ips:
        state[peer_ip] = dict()

        for f in _cache_files:
            stream = pybgpstream.BGPStream(data_interface="singlefile", filter="ipversion 4")
            stream.stream.set_data_interface_option("singlefile", "upd-file", f)

            for elem in stream:
                if elem.peer_address == peer_ip:
                    prefix = elem.fields['prefix']

                    if elem.type == 'A':
                        state[peer_ip][prefix] = elem.time

                    elif elem.type == 'W':
                        if prefix in state[peer_ip].keys():
                            time_passed = elem.time - state[peer_ip][prefix]

                            if time_passed > 0:
                                # filter out those with time 0
                                add_to_task4_result(peer_ip, prefix, time_passed, result)
                            state[peer_ip].pop(prefix, None)

        if len(state[peer_ip]) == 0:
            state.pop(peer_ip)

    return result


def add_to_task4_result(peer_ip, prefix, time_passed, result):
    if peer_ip not in result.keys():
        result[peer_ip] = dict()

    if prefix not in result[peer_ip].keys():
        result[peer_ip][prefix] = []

    result[peer_ip][prefix].append(time_passed)

# The main function will not be run during grading.
# You may use it however you like during testing.
#
# NB: make sure that check_solution.py runs your
#     solution without errors prior to submission
if __name__ == '__main__':
    # do nothing
    pass
