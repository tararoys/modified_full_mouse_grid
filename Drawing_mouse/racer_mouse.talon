-
start driving: user.racer_start()
stop driving: user.racer_stop()
car [gas | brake]: user.racer_gas_toggle()
car flip: user.racer_flip_turn_direction()
car nudge: user.racer_nudge()
car boost: user.racer_turbo_toggle()
car reverse: user.racer_reverse()

car {user.point_of_compass}: user.racer_set_direction(point_of_compass)
car <number>: user.racer_set_direction("{number}")

car random: user.racer_random()

#action(user.noise_hiss_start): user.racer_turn_start()
#action(user.noise_hiss_stop): user.racer_turn_stop()

#action(user.noise_pop): user.racer_gas_toggle()
