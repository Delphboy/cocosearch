import json
import argparse
from typing import List, Tuple

from torch import Tensor

class CocoCategory:
    super_category = None
    id = None
    name = None

    def __init__(self, id: int, super_category: str, name: str) -> None:
        self.id = id
        self.super_category = super_category
        self.name = name

    def __str__(self) -> str:
        return f"({self.id}, {self.super_category}, {self.name})"


class Coco():
    root = None
    images_root = None
    captions_root = None
    instances_root = None
    categories = {}
    instances = None

    def __init__(self, config_location) -> None:
        # read in config settings
        config_file = open(config_location)
        data = json.load(config_file)
        self.root = data["COCO"]["ROOT"]
        self.images_root = data["COCO"]["IMAGES"]
        self.captions_root = data["COCO"]["CAPTIONS"]
        self.instances_root = data["COCO"]["INSTANCES"]
        config_file.close()

        captions_file = open(self.captions_root)
        self.captions = json.load(captions_file)
        captions_file.close()

        instances_file = open(self.instances_root)
        self.instances = json.load(instances_file)
        instances_file.close()

        for category in self.instances["categories"]:
            self.categories[category["id"]] = CocoCategory(
                category["id"], category["supercategory"], category["name"]
            )

    def get_categories(self) -> dict:
        return self.categories

    def get_category_names(self) -> List[str]:
        names = []
        for key in self.categories.keys():
            names.append(self.categories[key].name)
        return names

    def get_category(self, id: int) -> CocoCategory:
        if id in self.categories.keys():
            return self.categories[id]
        else:
            return CocoCategory(-1, -1, "INVALID")

    def get_ids(self) -> List:
        image_ids = []
        for image in self.instances["images"]:
            image_ids.append(image["id"])
        return image_ids

    def get_complete_data_by_image_id(
        self, image_id: int
    ) -> Tuple[Tensor, List[str], List[CocoCategory]]:
        """Given an index, get:
        - image (as tensor)
        - 5 captions (as list)
        - object ids (as list)
        """
        image = None
        captions = None
        object_categories = None

        # TODO: Get the image so it can be returned

        # Get the captions
        captions = []
        for entry in self.captions["annotations"]:
            if entry["image_id"] == image_id:
                captions.append(entry["caption"])

        # get the object categories
        object_categories = []
        for annotation in self.instances["annotations"]:
            if annotation["image_id"] == image_id:
                object_categories.append(self.get_category(annotation["category_id"]))

        return image, captions, object_categories



def get_image_url(coco: Coco, id: int) -> str:
    for data in coco.instances['images']:
        if data['id'] == id:
            return data['coco_url']





def search_caption(coco: Coco, caption_search: str) -> None:
    caption_data = coco.captions['annotations']

    for cap in caption_data:
        if caption_search in cap['caption']:
            print(f"{cap['image_id']}:\n\t{cap['caption']}")


def search_id(coco: Coco, id:int) -> None:
    _, caps, cats = coco.get_complete_data_by_image_id(id)

    print(f"Image ID: {id}")
    for cap in caps:
        print(f"\t{cap}")

    print("")
    for cat in cats:
        print(f"\t{str(cat)}")

    print()
    print(f"\t{get_image_url(coco, id)}")
    

def main():
    parser = argparse.ArgumentParser(
        description="Search the COCO data set"
    )
    parser.add_argument("-c", "--caption",
        help="Search for term in captions",
        action="store",
        nargs=1,
        metavar=("caption_search")
    )
    parser.add_argument("-i", "--image_id",
        help="Returns data for a specific image ID",
        action="store",
        nargs=1,
        metavar=("image_id_search")
    )

    args = parser.parse_args()

    if args.caption is not None:
        coco_dataset = Coco("config.json")
        print(coco_dataset.get_ids()[:10])
        search_caption(coco_dataset, args.caption[0])

    if args.image_id is not None:
        coco_dataset = Coco("config.json")
        search_id(coco_dataset, int(args.image_id[0]))

if __name__ == "__main__":
    main()
