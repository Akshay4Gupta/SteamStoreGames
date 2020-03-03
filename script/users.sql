create table userDetails(userid text primary key, pass text);
insert into userDetails values('akshay', 'djflskjlksj');
insert into userDetails values('anant', 'djflskjlksj');
insert into userDetails values('aaditya', 'djflskjlksj');
insert into userDetails values('vivek', 'djflskjlksj');
insert into userDetails values('pd', 'djflskjlksj');
insert into userDetails values('komal', 'djflskjlksj');
insert into userDetails values('saswat', 'djflskjlksj');
insert into userDetails values('sagar', 'djflskjlksj');
insert into userDetails values('chinmay', 'djflskjlksj');
insert into userDetails values('kharthick', 'djflskjlksj');

create table cart(userid text, appid int, incartornot boolean default false, boughtornot boolean default false, primary key(userid, appid), foreign key(appid) references asteam(appid) on delete cascade, foreign key(userid) references userDetails(userid) on delete cascade);
insert into cart values('akshay', 2320, false);
insert into cart values('akshay', 31840);
insert into cart values('anant', 12540);
insert into cart values('aaditya', 31840, true);
insert into cart values('vivek', 2320);
insert into cart values('vivek', 65080, true, true);
insert into cart values('pd', 31840);
insert into cart values('komal', 8330);
insert into cart values('komal', 12540);
insert into cart values('komal', 9880);
insert into cart values('saswat', 98900);
insert into cart values('saswat', 204580);
insert into cart values('chinmay', 224460);
insert into cart values('kharthick', 24410);
insert into cart values('kharthick', 204580);
insert into cart values('sagar', 98900);


create table friends (userid1 text, userid2 text, primary key (userid1, userid2), foreign key(userid1) references userDetails(userid), foreign key(userid2) references userDetails(userid));
insert into friends values('akshay', 'vivek');
insert into friends values('anant', 'aaditya');
insert into friends values('akshay', 'aaditya');
insert into friends values('vivek', 'aaditya');
insert into friends values('pd', 'vivek');
insert into friends values('aaditya', 'komal');
insert into friends values('saswat', 'sagar');
insert into friends values('sagar', 'chinmay');
insert into friends values('chinmay', 'kharthick');







-- trigger that will awake when both values come true mainly when item is bought from the cart
create or replace function onezerofun()
  returns trigger as
  $$
    begin
      if new.boughtornot <> old.boughtornot and new.boughtornot = true then
        update cart set incartornot = false where incartornot = boughtornot;
      end if;
      return new;
    end;
  $$ language plpgsql;

create trigger onezero
  after update
  on cart
  for each row
  execute procedure onezerofun();

  create or replace function bot()
  returns trigger as
  $$
      begin
          if ((new.incartornot = new.boughtornot) and (new.incartornot = false or new.boughtornot = false)) then
              delete from cart where userid = old.userid;
          end if;
          return NEW;
      end;
  $$
  LANGUAGE plpgsql;

  create trigger removerow
  after update
  on cart
  for each row
  execute procedure bot();

-- (recommended friends) users that play atleast one same game and are not friends
create or replace view notfriends as select u1.userid as userid1 , u2.userid userid2 from userdetails u1, userdetails u2 where u1.userid <> u2.userid except (select userid1, userid2 from friends union select userid2, userid1 from friends);
create or replace view sameGame as select u1.userid as uid1, u2.userid as uid2, u1.appid from cart u1, cart u2 where u1.boughtornot = true and u2.boughtornot = true and u1.userid <> u2.userid and u1.appid = u2.appid;
select userid1, userid2 from sameGame, notfriends where userid1 = uid1 and userid2 = uid2;

-- (recommended game) users that are friends and returns a game that a friend plays but a user doesn't
create or replace view arefriends as select userid1, userid2 from friends union select userid2, userid1 from friends;
create or replace view diffgame as select distinct u1.userid as userid1 , u2.userid as userid2 from cart u1, cart u2 where u1.boughtornot = true and u2.boughtornot = true and u1.userid <> u2.userid and u1.appid <> u2.appid;



-- users that are not friends and play atleast one same game

-- users that are not our friends and play most games similar to ours
-- as2_7 mutual friends recommendations
create or replace view mutualfriends as select a1.userid1, a2.userid2 from arefriends a1, arefriends a2 where a1.userid2 = a2.userid1 and a1.userid1 <> a2.userid2 except select * from arefriends;
-- mutual friends games recommendations
create view personal as select * from mutualfriends where userid1 = 'akshay';
create view personalappid as select appid, userid2 from personal, cart where personal.userid1 = cart.userid and cart.boughtornot = true;
select distinct cart.appid from personalappid, cart where userid2 = userid and cart.appid <> personalappid.appid and boughtornot  = true except select distinct appid from personalappid;
-- no. of friends that doesn't play the same game
create view mygame as select appid from cart where userid = 'akshay' and boughtornot = true;
create view dummyfriends as select userid2 from arefriends where userid1 = 'akshay';
create view dummygames as select appid from dummyfriends, cart where userid2 = userid and boughtornot = true;
select * from dummygames except select * from mygame;
-- famous games for recommendations join with the personalized recommendations



-- games that are not played in our connected component but top the other connected components



-- create or replace view areConnected(uid1, uid2) as
-- 	with recursive test(uid1, uid2) as(
-- 		select * from arefriends
-- 		union
-- 		select arefriends.userid1, test.uid2
-- 		from arefriends, test
-- 		where arefriends.userid2 = test.uid1
-- 	)select * from test;
--
-- create or replace view allconnected(uid1, uid2) as
-- 	select * from areConnected
-- 	union
-- 	select userid as uid1, userid as uid2
-- 	from userdetails
-- 	where userid not in (select distinct(uid1) from areConnected);
--
-- create or replace view notinGroup select distinct uid2 from allconnected where uid1 = 'akshay';
--
-- create view gotit as select userid from userdetails except select * from notinGroup;
