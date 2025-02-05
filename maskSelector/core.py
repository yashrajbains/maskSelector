import os
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

# Initialize global variables
points = []
crop_points = []
mask = None


def load_fits_file():
    """Prompt user for FITS file and load data."""
    while True:
        file_name = input("Enter the FITS file name (with extension): ")
        if os.path.exists(file_name):
            hdu = fits.open(file_name)
            target_data = np.array(hdu[0].data, dtype=np.float64)
            wcs = WCS(hdu[0].header)
            print(f"File '{file_name}' loaded successfully.")
            return target_data, wcs
        else:
            print(f"File '{file_name}' not found.")


def select_crop_region(target_data):
    """User can select region to crop data."""
    global crop_points, rect
    crop_points = []
    rect = None
    confirmed = False

    def on_click(event):
        global rect
        if event.button == 1:  # Left mouse button
            crop_points.append((int(event.xdata), int(event.ydata)))
            print(f"Point selected: ({int(event.xdata)}, {int(event.ydata)})")

            if len(crop_points) == 2:
                x1, y1 = crop_points[0]
                x2, y2 = crop_points[1]
                x_start, x_end = sorted([x1, x2])
                y_start, y_end = sorted([y1, y2])

                width = x_end - x_start
                height = y_end - y_start

                if rect:
                    rect.remove()
                rect = Rectangle(
                    (x_start, y_start),
                    width,
                    height,
                    edgecolor="red",
                    facecolor="none",
                    linewidth=2,
                )
                ax.add_patch(rect)
                fig.canvas.draw()
                print(f"Crop region selected: x={x_start}-{x_end}, y={y_start}-{y_end}")

    def undo(event):
        """Resets the crop selection."""
        global rect, crop_points
        crop_points = []
        if rect:
            rect.remove()
            rect = None
        fig.canvas.draw()
        print("Crop selection reset.")

    def confirm(event):
        """Closes the window when the user confirms."""
        nonlocal confirmed
        confirmed = True
        plt.close(fig)


    # Plot the target data
    vmin, vmax = np.percentile(target_data, [3, 99.7])
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(target_data, cmap="viridis", norm=plt.Normalize(vmin=vmin, vmax=vmax))
    ax.set_title("Select crop region (click two points)")
    plt.grid()

    # Connect the click event
    cid = fig.canvas.mpl_connect("button_press_event", on_click)

    ax_undo = plt.axes([0.7, 0.02, 0.1, 0.05])  # Position (left, bottom, width, height)
    ax_confirm = plt.axes([0.81, 0.02, 0.1, 0.05])
    
    btn_undo = Button(ax_undo, 'Undo', color='red', hovercolor='darkred')
    btn_confirm = Button(ax_confirm, 'Confirm', color='green', hovercolor='darkgreen')

    btn_undo.on_clicked(undo)
    btn_confirm.on_clicked(confirm)


    plt.show()

    # Disconnect the event listener after the window is closed
    fig.canvas.mpl_disconnect(cid)

    if len(crop_points) < 2:
        print("No crop selected. Using full Image")
        return [(0, 0), (target_data.shape[1], target_data.shape[0])]
    return crop_points


def crop_data(target_data, crop_points):
    """Crop target data based on selected points."""
    x1, y1 = crop_points[0]
    x2, y2 = crop_points[1]
    x_start, x_end = sorted([x1, x2])
    y_start, y_end = sorted([y1, y2])
    cropped_data = target_data[y_start:y_end, x_start:x_end]
    print(f"Cropped data to x={x_start}-{x_end}, y={y_start}-{y_end}")
    return cropped_data


def save_cropped_data(cropped_data):
    """Prompt user for file name to save cropped data."""
    file_name = input("Enter name for cropped data file (without extension): ")
    np.save(f"{file_name}.npy", cropped_data)
    print(f"Cropped data saved as '{file_name}.npy'")


def create_mask(cropped_data):
    """User selects regions to mask."""
    global mask, points, rects
    mask = np.zeros_like(cropped_data, dtype=bool)
    points = []
    rects = []

    def on_click(event):
        global rects
        if event.button == 1:  # Left mouse button
            points.append((int(event.xdata), int(event.ydata)))
            print(f"Point selected: ({int(event.xdata)}, {int(event.ydata)})")

            if len(points) == 2:
                x1, y1 = points[0]
                x2, y2 = points[1]

                x_start, x_end = sorted([x1, x2])
                y_start, y_end = sorted([y1, y2])

                mask[y_start:y_end, x_start:x_end] = True
                print(f"Masked region: x={x_start}-{x_end}, y={y_start}-{y_end}")

                # Draw rectangle
                width = x_end - x_start
                height = y_end - y_start
                rect = Rectangle(
                    (x_start, y_start),
                    width,
                    height,
                    edgecolor="red",
                    facecolor="none",
                    linewidth=2,
                )
                ax.add_patch(rect)
                rects.append(rect)
                fig.canvas.draw()
                points.clear()

    def undo(event):
        """Removes last mask selection."""
        global rects, points
        if rects:
            rect = rects.pop()
            rect.remove()
            fig.canvas.draw()
            print("Last mask selection removed.")
        points.clear()

    def confirm(event):
        """Close window when confirmed."""
        plt.close(fig)

    # Plot cropped data
    vmin, vmax = np.percentile(cropped_data, [3, 99.7])
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(cropped_data, cmap="viridis", norm=plt.Normalize(vmin=vmin, vmax=vmax))
    ax.set_title("Select regions to mask (click two points)")
    plt.grid()

    cid = fig.canvas.mpl_connect("button_press_event", on_click)

    # Add buttons
    ax_undo = plt.axes([0.7, 0.02, 0.1, 0.05])  
    ax_confirm = plt.axes([0.81, 0.02, 0.1, 0.05])
    
    btn_undo = Button(ax_undo, 'Undo', color='red', hovercolor='darkred')
    btn_confirm = Button(ax_confirm, 'Confirm', color='green', hovercolor='darkgreen')

    btn_undo.on_clicked(undo)
    btn_confirm.on_clicked(confirm)
    
    plt.show()
    fig.canvas.mpl_disconnect(cid)
    return mask


def save_mask(mask):
    """Save mask to file."""
    file_name = input("Enter name for mask file (without extension): ")
    np.save(f"{file_name}.npy", mask)
    print(f"Mask saved as {file_name}.npy")


# core.py
def main():
    target_data, wcs = load_fits_file()
    crop_points = select_crop_region(target_data)
    cropped_data = crop_data(target_data, crop_points)
    save_cropped_data(cropped_data)
    mask = create_mask(cropped_data)
    save_mask(mask)

if __name__ == "__main__":
    main()
