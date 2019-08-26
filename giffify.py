from PIL import Image
import imageio

def create(base_name, i):
    fps = (i-1)/60
    kargs = {'duration': 0.5}
    with imageio.get_writer('Simulation\sim.gif', mode='I', **kargs) as writer:
        for j in range(i-1):
            filename = base_name + str(j) + '.png'
            frame = imageio.imread("Simulation\\" + filename)
            writer.append_data(frame)


