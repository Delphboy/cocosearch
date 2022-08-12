# cocosearch
A python based tool for looking things up in coco

# Installation

1. Clone repo
2. Install dependencies `pip install -r requirements.txt`
3. Download the COCO data set from https://cocodataset.org/#home
4. Configure the `config.json` file to point to the correct directories

# Usage

## Search Captions
Search for instances of a search term in captions

Example:

`python3 cocosearch.py --caption "lone bear"`

``` text
536292:
	A lone bear is walking in the woods.
489183:
	A lone bear walking in the woods in fall.
175057:
	A lone bear in the woods peering forward.
353306:
	A lone bear walking through a field of grass and flowers.
326011:
	A lone bear is walking in the wooded area.
203775:
	A lone bear wanders through a verdant field.
574720:
	A lone bear is walking in the tall grass and trees.
123891:
	A lone bear walking up a grassy hillside.
5745:
	a lone bear stands in the wilderness watching
```


## Search By Image ID
Search by Image ID to get the captions, object categories, and a link to view the image

`python3 coco.py --image_id 203775`

``` text
Image ID: 203775
	A grizzly bear in a brushy mountain meadow.
	A bear walking in the woods through the grass.
	Brown and white animal standing in an open field of grass.
	A lone bear wanders through a verdant field.
	a small animal stands in a brush area

	(23, animal, bear)

	http://images.cocodataset.org/train2017/000000203775.jpg
```

