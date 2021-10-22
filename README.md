# what the bot doin?
* spotter bot is a discord bot made because I am bored but not finished because I am not <b>THAT</b> bored.

* below is a quick guide for whoever wants to finish it.

# Necessary Additions

## Hosting the bot
* If you want to host the bot instead of running it locally there is a variety of hosting services

* A free option is [Heroku](https://devcenter.heroku.com/articles/dyno-types):
    * Heroku may reset and/or change your dynos location.
    * When that happens your most recent build will be redeployed meaning locally saved data will be erased.
    * To prevent that you can use Heroku's database. For more info see paragraph 'Setting up he database'
    * Note that your dynos' environment variables will not be erased.

## Updating Environment Variables

* The bot token must be set as an environment variable on the system the bot is running on

* To do so you may follow [this tutorial](https://www.schrodinger.com/kb/1842). If you are running the bot locally or follow the instructions of your application host

## Setting up he database

* If you want to run your bot on a remote server it's best to not litter it with locally saved files

* If you are running on Heroku you can use it's [postgres DB](https://www.heroku.com/postgres).

* The database can be set up as a single table using the user's discord id as a primary key and store their score in a second row.
    * (not very shiny but nobody said it had to be)

#### Modifying the bot's code

* below are the two functions implementing an imaginary library to connect to a database:

```python
import db_library


def db_lookup(id):
    con = db_library.connect("""(This is a secret url to the db.
                            Your remote host might already provide
                            an environment var for it)""")
    
    cur = con.cursor()
    cur.execute(f"""IF NOT EXISTS (SELECT score FROM player_table
                                    WHERE id like {id})
                    BEGIN
                        INSERT INTO player_table (id, score)
                        VALUES ({id}, 0)
                    END""")
                    
    
    spotting_total = cur.fetchone(f"""SELECT score FROM player_table
                                    WHERE id like {id}""")
    con.close()
    
    
    return spotting_total


# update the user's spotting score after scoring
def db_update(id, new_total):
    con = db_library.connect("""(This is a secret url to the db.
                            Your remote host might already provide
                            an environment var for it)""")
    
    cur = con.cursor()
    cur.execute(f"""UPDATE player_table
                    SET score = {new_total}
                    WHERE id like {id}
    """)
    
    con.close()
```

* note that this is not optimized nor is it tested. so don't expect this to work :)
