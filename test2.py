
max_health = 10000
remaining_health = 1000
health_bar = 75 

pixel_per_percent = health_bar / (max_health / remaining_health)
remaining_health_percent = remaining_health / max_health * 100

print('health remaining:',remaining_health_percent,'%')
print('pixels per percent',pixel_per_percent)
print(pixel_per_percent * remaining_health_percent)


pixel_per_percent = 75 / (ship.max_health / ship.remaining_health)