import random
from .Cloud import Cloud
from src.Utils.GAME_conf import WIDTH, HEIGHT


class CloudManager:
	MAX_CLOUDS = 10  # Max number of clouds created at the time
	CLOUD_DENSITY = 1  #

	MIN_DISTANCE_BETWEEN_CLOUDS_X = 100  # horizontal distance in pixels
	MAX_DISTANCE_BETWEEN_CLOUDS_X = 200  # horizontal distance in pixels
	
	MIN_DISTANCE_BETWEEN_CLOUDS_Y = 150  # min vertical distance in pixels
	MAX_DISTANCE_BETWEEN_CLOUDS_Y = 200  # max vertical distance in pixels
	
	def __init__(self):
		self.clouds: [Cloud] = []
		self._generate_new_clouds_if_necessary()
	
	def _generate_cloud_coordinates(self, previous_cloud_y) -> (int, int):
		new_cloud_y_distance = random.randint(self.MIN_DISTANCE_BETWEEN_CLOUDS_Y, self.MAX_DISTANCE_BETWEEN_CLOUDS_Y)
		
		new_cloud_x = random.randint(0, WIDTH-Cloud.AVERAGE_WIDTH)
		new_cloud_y = previous_cloud_y - new_cloud_y_distance
		
		return new_cloud_x, new_cloud_y
	
	def _generate_clouds_coordinates(self) -> [(int, int)]:
		new_clouds_number = self.MAX_CLOUDS-len(self.clouds)
		if len(self.clouds) > 1:
			previous_cloud_y = min(max(self.clouds, key=lambda obj: obj.y).y, -100)
		else:
			previous_cloud_y = HEIGHT//3-self.MIN_DISTANCE_BETWEEN_CLOUDS_Y*len(self.clouds)

		clouds_coordinates = []
		for _ in range(new_clouds_number):
			new_cloud_coo = self._generate_cloud_coordinates(previous_cloud_y)
			clouds_coordinates.append(new_cloud_coo)
			previous_cloud_x, previous_cloud_y = new_cloud_coo
			
		return clouds_coordinates
		
	def _generate_new_clouds_if_necessary(self):
		for i in range(self.CLOUD_DENSITY):
			[self.clouds.append(Cloud(coo[0], coo[1])) for coo in self._generate_clouds_coordinates()]
	
	def update(self, ds: int):
		# ds is the instant downwards speed of the world. it is calculated like main_character_speed * dt
		# First the clouds are moven downwards to simulate the main character going up
		[cloud.update(ds) for cloud in self.clouds]
		# the clouds that go outside the screen are removed from the world
		self.clouds = [cloud for cloud in self.clouds if cloud.is_inside_screen()]
		# new clouds are created if necessary to replace the removed ones
		self._generate_new_clouds_if_necessary()
	
	def draw_clouds_in_front_of_character(self, screen):
		[cloud.draw(screen) for cloud in self.clouds if cloud.layer >= 0]
	
	def draw_clouds_behind_character(self, screen):
		[cloud.draw(screen) for cloud in self.clouds if cloud.layer < 0]
