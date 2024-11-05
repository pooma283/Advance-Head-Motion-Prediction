#!/usr/bin/env python3

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import argparse
import numpy as np


def main():
     # CSV column indices
     T=0
     X=1
     Y=2
     Z=3
     QX=4
     QY=5
     QZ=6
     QW=7
     ROLL=8
     PITCH=9
     YAW=10

     # Head translation values
     x=[]
     y=[]
     z=[]

     # Head rotation values (as normal vector)
     u=[]
     v=[]
     w=[]

     # Normal vector for rotation of the head pointing in z-direction
     head_normal = [0,0,-1]

     # Converts a quaternion to euler angles
     def q2e(q):
          r = R.from_quat([q[0], q[1], q[2], q[3]])
          r = r.as_euler('ZXY', degrees=True)
          return [r[0], r[1], r[2]]

     with open(args.file[0]) as csvfile:
          reader = csv.reader(csvfile, delimiter=',')
          line=0
          sensor_sample_time=5 # in ms
          plot_sample_time=100 # in ms
          skip=plot_sample_time / sensor_sample_time
          for row in reader:
               # skip csv header and reduce the data points to render by skipping values
               if line>0 and line%skip==0:
                    #rotation = R.from_euler('ZXY', row[ROLL:YAW+1], degrees=True)
                    rotation = R.from_quat(row[QX:QW+1])
                    vec = rotation.apply(head_normal)

                    x.append(float(row[X]))
                    y.append(float(row[Y]))
                    z.append(float(row[Z]))
                    u.append(float(vec[0]))
                    v.append(float(vec[1]))
                    w.append(float(vec[2]))
               else:
                    pass
               line += 1

     if args.animate:
          render_pose_animated(x,y,z,u,v,w)
     else:
          render_pose_static(x,y,z,u,v,w)


def render_pose_static(x,y,z,u,v,w):
     mpl.rcParams['legend.fontsize'] = 10

     fig = plt.figure()
     ax = fig.gca(projection='3d')
     ax.quiver(x, z, y, u, w, v, arrow_length_ratio=0.3, pivot='middle', length=0.1, label='Head Pose')
     ax.scatter(x[1:-2], z[1:-2], y[1:-2])
     ax.scatter(x[0], z[0], y[0], color='Green', linewidths=10, label='Start Point')
     ax.scatter(x[-1], z[-1], y[-1], color='Orange', linewidths=10, label='Stop Point')
     ax.legend()

     ax.set_xlabel('x')
     ax.set_ylabel('z')
     ax.set_zlabel('y')
     fig=plt.gcf()
     plt.show()

     if args.save is not None:
          fig.savefig(args.save)

def render_pose_animated(x,y,z,u,v,w):
     fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

     def get_arrow(theta):
          return x[theta],z[theta],y[theta],u[theta],w[theta],v[theta]

     quiver = ax.quiver(*get_arrow(0), pivot='middle')

     ax.set_xlim(-2, 2)
     ax.set_ylim(-2, 2)
     ax.set_zlim(-2, 2)

     def update(theta):
          nonlocal quiver
          quiver.remove()
          quiver = ax.quiver(*get_arrow(theta), label='Head Pose', pivot='middle')
          ax.legend()

     ani = FuncAnimation(fig, update, frames=range(0,len(x), 1), interval=5, save_count=len(x))

     ax.set_xlabel('x')
     ax.set_ylabel('z')
     ax.set_zlabel('y')
     plt.show()

     if args.save is not None:
          ani.save(args.save)

if __name__ == '__main__':
     ap = argparse.ArgumentParser(description='Renders a users head pose')
     ap.add_argument('-a', '--animate', action='store_true', required=False, help='Animates the head pose')
     ap.add_argument('-s', '--save', metavar='FILE', required=False, help='Saves the rendered view to a file. The extension determines the type.')
     ap.add_argument('file', metavar='FILE', nargs=1, help='Path to a csv file containing head poses')
     args=ap.parse_args()
     main()