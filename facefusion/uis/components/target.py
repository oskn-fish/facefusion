from typing import Tuple, Optional
import gradio

import facefusion.globals
from facefusion import wording
from facefusion.face_store import clear_static_faces, clear_reference_faces
from facefusion.uis.typing import File
from facefusion.filesystem import is_image, is_video
from facefusion.uis.core import register_ui_component

TARGET_FILE : Optional[gradio.File] = None
TARGET_IMAGE : Optional[gradio.Image] = None
TARGET_VIDEO : Optional[gradio.Video] = None

TARGET_GRADIO_IMAGE = None
TARGET_GRADIO_VIDEO = None
TARGET_FILE_PATHS = None


def render(target_ui) -> None:
	global TARGET_FILE
	global TARGET_IMAGE
	global TARGET_VIDEO

	is_target_image = is_image(facefusion.globals.target_path)
	is_target_video = is_video(facefusion.globals.target_path)
	TARGET_FILE = gradio.File(
		label = wording.get('target_file_label'),
		file_count = 'single',
		file_types =
		[
			'.png',
			'.jpg',
			'.webp',
			'.mp4'
		],
		value = facefusion.globals.target_path if is_target_image or is_target_video else None
	)
	TARGET_IMAGE = gradio.Image(
		value = TARGET_FILE.value['name'] if is_target_image else None,
		visible = is_target_image,
		show_label = False
	)
	TARGET_VIDEO = gradio.Video(
		value = TARGET_FILE.value['name'] if is_target_video else None,
		visible = is_target_video,
		show_label = False
	)
	register_ui_component('target_image', TARGET_IMAGE)
	register_ui_component('target_video', TARGET_VIDEO)
	target_ui.load(restore, outputs = [ TARGET_FILE, TARGET_IMAGE, TARGET_VIDEO ])


def listen() -> None:
	TARGET_FILE.change(update, inputs = TARGET_FILE, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])

def restore() -> None:
    return TARGET_FILE_PATHS, TARGET_GRADIO_IMAGE, TARGET_GRADIO_VIDEO

def update(file : File) -> Tuple[gradio.Image, gradio.Video]:
	global TARGET_GRADIO_IMAGE
	global TARGET_GRADIO_VIDEO
	global TARGET_FILE_PATHS
	clear_reference_faces()
	clear_static_faces()
	TARGET_FILE_PATHS = file.name
	if file and is_image(file.name):
		facefusion.globals.target_path = file.name
		TARGET_GRADIO_IMAGE, TARGET_GRADIO_VIDEO = gradio.Image(value = file.name, visible = True), gradio.Video(value = None, visible = False)
		return TARGET_GRADIO_IMAGE, TARGET_GRADIO_VIDEO
	if file and is_video(file.name):
		facefusion.globals.target_path = file.name
		TARGET_GRADIO_VIDEO, TARGET_GRADIO_VIDEO = gradio.Image(value = None, visible = False), gradio.Video(value = file.name, visible = True)
		return TARGET_GRADIO_IMAGE, TARGET_GRADIO_VIDEO
	facefusion.globals.target_path = None
	return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)
