import math

# visualisation
import matplotlib.pyplot as plt
import matplotlib.lines as lines
# visualisation

def Sum_points(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    return x1+x2, y1+y2

def Multiply_point(multiplier, P):
    x, y = P
    return float(x)*float(multiplier), float(y)*float(multiplier)

def Check_if_object_is_polygon(Cartesian_coords_list):
    if Cartesian_coords_list[0] == Cartesian_coords_list[len(Cartesian_coords_list)-1]:
        return True
    else:
        return False

class Object():

    def __init__(self, Cartesian_coords_list):
        self.Cartesian_coords_list = Cartesian_coords_list

    def Find_Q_point_position(self, P1, P2):
        Summand1 = Multiply_point(float(3)/float(4), P1)
        Summand2 = Multiply_point(float(1)/float(4), P2)
        Q = Sum_points(Summand1, Summand2)
        return Q

    def Find_R_point_position(self, P1, P2):
        Summand1 = Multiply_point(float(1)/float(4), P1)
        Summand2 = Multiply_point(float(3)/float(4), P2)
        R = Sum_points(Summand1, Summand2)
        return R

    def Smooth_by_Chaikin(self, obj, number_of_refinements):
        refinement = 1
        copy_first_coord = Check_if_object_is_polygon(self.Cartesian_coords_list)
        while refinement <= number_of_refinements:
            self.New_cartesian_coords_list = []

            for num, tuple in enumerate(self.Cartesian_coords_list):
                if num+1 == len(self.Cartesian_coords_list):
                    pass
                else:
                    P1, P2 = (tuple, self.Cartesian_coords_list[num+1])
                    Q = obj.Find_Q_point_position(P1, P2)
                    R = obj.Find_R_point_position(P1, P2)
                    self.New_cartesian_coords_list.append(Q)
                    self.New_cartesian_coords_list.append(R)

            if copy_first_coord:
                self.New_cartesian_coords_list.append(self.New_cartesian_coords_list[0])

            self.Cartesian_coords_list = self.New_cartesian_coords_list
            refinement += 1
        return self.Cartesian_coords_list

def smoothPolygon(points):
    Cartesian_coords_list = points

    obj = Object(Cartesian_coords_list)
    Smoothed_obj = obj.Smooth_by_Chaikin(obj, number_of_refinements=15)

    # visualisation
    x1 = [i for i, j in Smoothed_obj]
    y1 = [j for i, j in Smoothed_obj]
    # x2 = [i for i, j in Cartesian_coords_list]
    # y2 = [j for i, j in Cartesian_coords_list]

    #plt.plot(range(2), range(2), 'w', alpha=0.7)

    # plt.text(x1[0], y1[0], "0")
    # plt.text(x1[int(len(x1) / 4)], y1[int(len(x1) / 4)], "1")
    # plt.text(x1[int(len(x1) / 2)], y1[int(len(x1) / 2)], "2")
    # plt.text(x1[int(len(x1) / 1.33)], y1[int(len(x1) / 1.33)], "3")

    # myline = lines.Line2D(x1, y1, color='r')
    # #mynewline = lines.Line2D(x2, y2, color='b')
    # plt.gca().add_artist(myline)
    # # plt.gca().add_artist(mynewline)
    # plt.show()

    #print(Smoothed_obj)
    print(len(Smoothed_obj))
    return Smoothed_obj

if __name__ == "__main__":

    Cartesian_coords_list = []

    with open("poly.txt", "r") as txt_file:
        for line in txt_file.readlines():
            vertex = line.split(" ")
            x = float(vertex[0])
            y = float(vertex[1])

            Cartesian_coords_list.append((x, y))


    # Cartesian_coords_list = [(1,1),
    #                          (1,3),
    #                          (4,5),
    #                          (5,1),
    #                          (2,0.5),
    #                          (1,1),
    #                          ]

    obj = Object(Cartesian_coords_list)
    Smoothed_obj = obj.Smooth_by_Chaikin(number_of_refinements = 15)

    # visualisation
    x1 = [i for i,j in Smoothed_obj]
    y1 = [j for i,j in Smoothed_obj]
    x2 = [i for i,j in Cartesian_coords_list]
    y2 = [j for i,j in Cartesian_coords_list]
    plt.plot(range(2),range(2),'w', alpha=0.7)


    plt.text(x1[0], y1[0], "0")
    plt.text(x1[int(len(x1) / 4)], y1[int(len(x1) / 4)], "1")
    plt.text(x1[int(len(x1) / 2)], y1[int(len(x1) / 2)], "2")
    plt.text(x1[int(len(x1) / 1.33)], y1[int(len(x1) / 1.33)], "3")

    myline = lines.Line2D(x1,y1,color='r')
    mynewline = lines.Line2D(x2,y2,color='b')
    plt.gca().add_artist(myline)
   # plt.gca().add_artist(mynewline)
    plt.show()
