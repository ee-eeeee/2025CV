from ultralytics.data.converter import convert_coco

# For keypoints data (like person_keypoints_val2017.json)
convert_coco(
    labels_dir="/home/uav_dataset/ann",  # Directory containing your json file
    save_dir="/home/uav_dataset/labels/",
    use_keypoints=False,
    cls91to80=False  # Since you're using keypoints data
)
