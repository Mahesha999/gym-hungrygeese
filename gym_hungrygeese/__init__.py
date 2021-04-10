from gym.envs.registration import register

register(
    id='hungrygeese-v0',
    entry_point='gym_hungrygeese.envs:HungryGeeseEnv',
)