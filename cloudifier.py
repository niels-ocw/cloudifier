''' this program ilustrates the grouping of pixels that touch eachother horizontally or vertically.
    just like the movement of a rook across a chessboard.
    the resulting output are pictures of which the first one displays horizontally touching pixels
    in each row having the same color.
    the second picture shows the result after those horizontal lines have been merged vertically.
    in this second picture all pixels sharing a vertical or horizontal border have the same color.
    you can modify frame_count, w, h to change output. '''

import time
from sys import exit
from PIL import Image, ImageSequence
from matplotlib import pyplot as plt
import random

# frame_count determines the number of output picture pairs to be displayed
frame_count = 1


def main():

    # width and height in pixels (need be equal)
    # recommended range: [3, 30]
    w, h = 6, 6
    clouds_L_green = []

    for i in range(frame_count):
        temp = Image.new("L", (w, h))
        clouds_L_green.append(temp)

    # creating the random pixelmap
    for i in range(frame_count):
        white_px_list = [(random.randint(0,h-1), random.randint(0,h-1)) for i in range(random.randint(0,w*h))]

        for px in white_px_list:
            (y, x) = px
            clouds_L_green[i].putpixel((x,y), 255)

    ''' cloudlines[{}, {}, ...] <<< clouds_L_green[] '''

    ''' (1) grouping all neighbouring pixels in each y-row in groups identified by cloudline_nr '''

    w, h = clouds_L_green[0].size

    # cloudlines contains lists per frame
    # these lists contain coordinate collection lists per horizontally touching pixels: called cloud rows or cloud lines
    # cloudlines[i][0] thus gives a list containing all coordinate tuples that belong to cloud number 0:
    # cloudlines[i][cloudline_nr] = [(yx), ...], and
    # cloudlines[i][cloudline_nr][3].append(x) appends coordinate to list
    # cloudline_nr is actually the index of the sub arrays
    #
    # fill the cloudlines with empty lists for easier access in next for loop
    cloudlines = [[] for i in range(frame_count)]

    # cloud number map per pixel: gives the corresponding cloudline_nr for each pixel(x,y) 
    # each frame gets its own cloud number reference per pixel
    # cloudline_nrs_map[frame=i][y=y][x=x] = -1 <default values> = cloudline_nr
    cloudline_nrs_map = [[[-1 for x in range(w)] for y in range(h)] for i in range(frame_count)]

    for i in range(frame_count):
        cloudline_nr = -1

        for y in range(h):
            # last_p == True if last pixel considered in loop was a cloud/was p=255
            last_p = False

            for x in range(w):
                # pixel returned is either 0: no cloud, or 255: yes cloud
                p = clouds_L_green[i].getpixel((x, y))
                
                # last pixel not cloud AND current pixel not cloud
                if last_p == False and p == 0:
                    pass
                
                # last pixel not cloud AND current pixel IS cloud
                elif last_p == False and p == 255:
                    cloudline_nr = cloudline_nr + 1
                    last_p = True

                    # init new cloudline:
                    # cloudline = [group_nr, cloudline_nr, y, [x0, x1, ..] ]
                    cloudlines[i].append([-1, cloudline_nr, y, []])
                    # append x coordinates:
                    cloudlines[i][cloudline_nr][3].append(x)

                    # put cloudline_nr into map; replace the -1 by cloudline_nr
                    cloudline_nrs_map[i][y][x] = cloudline_nr

                elif last_p == True and p == 0:
                    last_p = False

                elif last_p == True and p == 255:
                    # append x coordinates:
                    cloudlines[i][cloudline_nr][3].append(x)

                    # put cloudline_nr into map; replace the -1 by cloudline_nr
                    cloudline_nrs_map[i][y][x] = cloudline_nr

    ''' (2.v.3) connecting all vertically adjacent y-rows in groups identified by cloud_id (IS NOT cloudline_nr) '''
    ''' notes pages 20, .. '''

    # after next loop groups[i] will contain groups[i] = groups[GROUP_NR] =
    groups = [ [] for i in range(frame_count) ]
    group_nr_for_lines = [ [] for i in range(frame_count) ]

    for i in range(0, frame_count):

        groups_i = groups[i]
        # list of all line#'s in this frame:
        all_line_nrs = [ n for n in range(len(cloudlines[i])) ]
        unassigned = set(all_line_nrs)
        group_nr_for_line = dict([ (n, None) for n in all_line_nrs ])
        # G is last MAIN group#:
        G = -1
        # small-g is current group#
        g = None

        # n = cloudline_nr
        for n in all_line_nrs:
            ''' if len(unassigned) = 0 >>> continue, all lines are already assigned '''
            ''' though i guess this will rarely happen '''
            ''' more likely that theres a stray pixel somewhere '''

            current_line = cloudlines[i][n]
            X = current_line[3]  # = [x0..xn]
            y = current_line[2]

            if group_nr_for_line[n] == None:
                # line is ungrouped: create new group and assign line to it:
                groups_i.append(set())  # groups[i] = [{ <filled with cloudline_nr's> }, ..]
                G = G + 1 # G is now at right index: groups_i[G] = groups[i][G] = set() :: references current group set
                # small-g is current group#
                g = G

                # add n to dict and to group-set:
                current_group = groups_i[g]
                group_nr_for_line[n] = g
                current_group.add(n)

                # remove n from the unassigned set:
                # remove newly assigned line-nrs from the unassigned set
                unassigned.remove(n)
            else:
                # line is already grouped into group g: get its group number:
                g = group_nr_for_line[n]

            new_neighbors = set()  # {}
            ass_neighbors = set()  # {}

            # check north neighbors:
            if not y == 0:
                for x in X:
                    # get line# for this (x,y):
                    line_nr = cloudline_nrs_map[i][y - 1][x]

                    if not line_nr == -1:
                        if line_nr in unassigned:
                            # current_group.add(n)
                            new_neighbors.add(line_nr)

                        else:
                            # if already assigned
                            ass_neighbors.add(line_nr)

            # check south neighbors:
            if y < h - 1:
                for x in X:
                    # get line# for this (x,y):
                    line_nr = cloudline_nrs_map[i][y + 1][x]

                    # ({y},{x}) S ({y+1},{x}) >> line_nr={line_nr}
                    if not line_nr == -1:
                        if line_nr in unassigned:
                            # current_group.add(n)
                            new_neighbors.add(line_nr)

                        else:
                            # if already assigned
                            ass_neighbors.add(line_nr)

            # neighbors check is now complete
            # update new neighbors's line# to group# mapping:
            for line_nr in new_neighbors:
                # delete me:
                if not group_nr_for_line[line_nr] == None:
                    print("This shouldn't happen")
                    exit(1)

                # assign groupnr to linenr:
                group_nr_for_line[line_nr] = g

            # put new_neighbors's members into current group
            current_group = groups_i[g]
            current_group.update(new_neighbors)

            # remove newly assigned line-nrs from the unassigned set
            for nrs in new_neighbors:
                unassigned.remove(nrs)

            if ass_neighbors: #== line numbers
                # get group numbers of assigned neighbors:

                # n = current line nr:
                if n not in ass_neighbors:
                    ass_neighbors.add(n)

                ass_neighbor_group_nrs = set()
                for nrs in ass_neighbors:
                    ass_neighbor_group_nrs.add(group_nr_for_line[nrs])

                # no need to add g to determine if it has the lowest group number,
                # was already done via n at beginning

                # determine the leading groupnumber: this is the lowest from the set
                leader = min(ass_neighbor_group_nrs)  # leader = group nr
                mergers = ass_neighbor_group_nrs  # mergers = group nrs
                if leader in ass_neighbor_group_nrs:
                    mergers.remove(leader)

                # now we have the leader group and all other groups are mergers to be merged into the leader group

                # merge:
                # (1) update dict: overwrite old groupnumbers to new leader groupnumber:
                for g_nr in mergers:  # mergers = group nrs
                    for merger_line_number in groups_i[g_nr]:
                        group_nr_for_line[merger_line_number] = leader

                # (2) put mergers into leader group AND
                # (3) delete/empty/clear the merger groups
                leader_group = groups_i[leader] # leader = group nr
                for g_nr in mergers:  # mergers = group nrs
                    merger_group_i = groups_i[g_nr]
                    leader_group.update(merger_group_i)

                    merger_group_i.clear()
        
        
        group_nr_for_lines[i] = group_nr_for_line

    # updating pixel_group_nrs_map
    pixel_group_nrs_map = [[[-1 for x in range(w)] for y in range(h)] for i in range(frame_count)]
    
    for i in range(frame_count):
		# printing results
        print("groups[i] contains sets of cloudline numbers from the first output image beginning at 0")
        print("cloudlines in the same set have the same color in the second output image")
        print("(remember: cloudlines can contain multiple (x,y)-coordinates)\n")
        print(f"groups[i={i}] = {groups[i]}\n")
        
        for group in groups[i]:
            
            for line_nr in group:
                current_line = cloudlines[i][line_nr]
                X = current_line[3]  # = [x0..xn]
                y = current_line[2]
                
                g = group_nr_for_lines[i][line_nr]

                for x in X:
                    pixel_group_nrs_map[i][y][x] = g
    
    # plotting results
    for i in range(0, frame_count):
        plot(cloudline_nrs_map[i])
        plot(pixel_group_nrs_map[i])

    ''' exit(0) moved into maintime() '''


# the plot command will halt the program flow until plot window is closed
# requires: from matplotlib import pyplot as plt
def plot(image):

    plt.imshow(image, interpolation='nearest')
    # figure title:
    # plt.title("Title")
    # window title:
    fig = plt.gcf()
    # fig.canvas.set_window_title('My title')
    fig.canvas.set_window_title(str(image))
    plt.show()


# executes main() and measures execution times
# from: "04-timeit-test.py"
def maintime():

    '''requires "import time"'''
    # before times:
    time_0_pc = time.perf_counter()
    time_0_pt = time.process_time()
    # function call:
    main()
    # Total time {including waits}:
    time_t_pc = time.perf_counter()
    delta_pc = time_t_pc - time_0_pc
    print(f"Grand Total : {delta_pc:.3f} [s]")
    # Pure process time:
    time_t_pt = time.process_time()
    delta_pt = time_t_pt - time_0_pt
    print(f"Process Time: {delta_pt:.3f} [s]")
    exit(0)


''' main() runs from maintime() '''
maintime()
