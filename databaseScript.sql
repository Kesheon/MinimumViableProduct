USE master
GO
if DB_ID('GameConnect') is null
	Create Database GameConnect;
GO

USE GameConnect
GO

create Table Account(
AccountId varchar(5),
IsStore BIT,
Latitude DECIMAL(10,8),
Longitude DECIMAL(11,8),
UserName varchar(17),
Bio varchar(550),
AccountPass varchar(17)
UNIQUE(AccountId),
primary key(AccountId)
);

go

Create Table Games(
GameName varchar(20),
Bio varchar(600),
Tools varchar(200),
UNIQUE(GameName),
primary key(GameName)
);

go

Create Table Account2Game(
AccountId varchar(5) not null,
GameName varchar(20) not null,
RankOfInterest int,
FOREIGN KEY(AccountId) REFERENCES Account(AccountId),
FOREIGN KEY(GameName) REFERENCES Games(GameName)
)

go

Create Table _Message(
Sender varchar(5) not null,
Receiver varchar(5) not null,
BottleContent varchar(500) not null,
MessageTime  dateTime,
FOREIGN KEY(Sender) REFERENCES Account(AccountId),
FOREIGN KEY(Receiver) REFERENCES Account(AccountId)
)

go 

create table Vender_Reviews(
AccountId varchar(5) NOT null, 
Title varchar(20) not null,
review varchar(600) not null,
ReviewDate dateTime,
foreign key(AccountId) references Account(AccountId)
)

go 

Create table RLEvent(
Latitude DECIMAL(10,8),
Longitude DECIMAL(11,8),
Title varchar(20) not null,
Decription varchar(600) not null,
Host varchar(5) not null,
foreign key(Host) references Account(AccountId)
)