OpenAI gym for kaggle [hungry geese competition](https://www.kaggle.com/c/hungry-geese) environment.

CD to `gym-hungrygeese` (note `-` not `_`, that is the directory containing `setup.py`) and run `pip install -e gym-hungrygeese`
Gym created following instructions [here](https://github.com/openai/gym/blob/master/docs/creating-environments.md).

After installation, you should be able to do:

```
>>> import gym
>>> env = gym.make('gym_hungrygeese:hungrygeese-v0')
```
