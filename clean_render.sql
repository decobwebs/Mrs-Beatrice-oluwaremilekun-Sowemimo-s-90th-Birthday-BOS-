--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: guest; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.guest (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    guest_type_id integer NOT NULL
);


--
-- Name: guest_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.guest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: guest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.guest_id_seq OWNED BY public.guest.id;


--
-- Name: guest_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.guest_type (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: guest_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.guest_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: guest_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.guest_type_id_seq OWNED BY public.guest_type.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(200) NOT NULL,
    role character varying(20) NOT NULL
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: guest id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest ALTER COLUMN id SET DEFAULT nextval('public.guest_id_seq'::regclass);


--
-- Name: guest_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest_type ALTER COLUMN id SET DEFAULT nextval('public.guest_type_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
d2878df7acbd
\.


--
-- Data for Name: guest; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.guest (id, name, email, phone, "timestamp", guest_type_id) FROM stdin;
72	Olatunji Idowu Mariam 	ojimiidowu@gmail.com	08033866390	2025-03-20 05:45:28.553734	16
73	Ibikunle Phillips	ibikunlephillips@gmail.com	08038456457	2025-03-20 06:11:40.529586	16
24	ITEOGU FRED	iteogufred@gmail.com	08036245766	2025-03-18 10:44:13.939471	16
25	Flora Tijani 	florabnj@yahoo.co.uk	08137445909	2025-03-18 10:45:48.087406	16
26	Oluranti Williams	olurantiwilliams7@gmail.com	08062097741	2025-03-18 10:56:37.204043	16
27	Ifeoma Okoro	okoro.ifeoma17@gmail.com	07034275949	2025-03-18 11:27:38.411095	16
28	Olukoya Gbenga	g.bengs@yahoo.com	08032093616	2025-03-18 11:48:26.162202	16
29	Omobolanle Adebanjo 	Bladebanjo@yahoo.com	7135500708	2025-03-18 12:34:44.636866	16
30	Opemipoo Osonaike	lizmawi@yahoo.com	08036758004	2025-03-18 19:12:03.340371	16
31	Nkechinyere Ofili 	nkechinyereuka@yahoo.com	08037030216	2025-03-18 19:14:27.591544	16
32	Jide Afolabi 	jhitechinnovations@gmail.com	08036686109	2025-03-18 19:15:06.008116	16
33	Temilola Onasanya 	temiyeye@yahoo.com	08181449827	2025-03-18 19:16:42.503591	16
34	Oluwafunke  Oluwatula 	funkeoluwatula@gmail.com	6123889293	2025-03-18 19:24:05.560874	16
35	Sola Abe	abe.sola@gmail.com	08038140132	2025-03-18 19:37:07.502968	16
36	Mr & Mrs Airewele	adesolaairewele@yahoo.com	08029480258	2025-03-18 19:37:51.005462	16
37	Adetoun Odugbemi 	tounodugbemi@gmail.com	08054135344	2025-03-18 19:47:17.682026	16
38	Rita ojeifo 	ritaojeifo@gmail.com	08137517669	2025-03-18 20:01:54.505109	16
39	Oludare Tijani	daretijani@gmail.com	08023116849	2025-03-18 20:11:43.909866	16
40	Yewande Oyewole	yewande1985@gmail.com	08181375410	2025-03-18 20:16:14.150671	16
41	Fola Elufowoju 	blessfola@yahoo.ca	07801737962	2025-03-18 20:21:40.122171	16
42	Rita ojeifo 	destinyojeifo93@gmail.com	08137517669	2025-03-18 20:30:00.231801	16
43	Olukayode Amu	johnsonoamu@gmail.com	+447793210920	2025-03-18 20:45:06.977372	16
44	Titi	titiola247@gmail.com	08023164582	2025-03-19 05:54:25.393561	16
45	Osonaike Oladimeji	osonaike@yahoo.co.uk	07040001246	2025-03-19 06:30:13.198634	16
46	Olatunji Akinwale Anthony 	akinwaleolatunji77@gmail.com	08081554788	2025-03-19 08:56:38.678225	16
47	Ekpema Uko	ekpes@yahoo.com	08055464300	2025-03-19 08:57:03.425165	16
48	Enobong Uko	enoenookon2002@yahoo.com	08035371854	2025-03-19 08:58:21.87108	16
49	Adegoke  Adeniyi 	adegokeadeniyi@gmail.com.com	08168056369	2025-03-19 08:59:26.472315	16
50	Taiwo Ebenezer abayomi 	chairmanabcon@yahoo.com	08035033038	2025-03-19 09:01:31.418963	16
51	Bolanle Kareem 	bolaboy01@yahoo.com	+2348069529320	2025-03-19 09:03:34.406476	16
52	Mr & Mrs Abbey	olusoladavid49@gmail.com	07039612341	2025-03-19 09:05:12.964827	16
53	Mr. Abbey Oluwashola 	olusholadavid49@gmail.com	07039612341	2025-03-19 09:15:32.599548	16
54	Uwatomo 	omolayeuwa@gmail.com	08055261422	2025-03-19 09:17:29.789847	16
55	Mrs Abbey Omowunmi 	wunmishola@gmail.com	07062556662	2025-03-19 09:18:05.652203	16
56	Oladiran Oluyide Reuben 	princeolu_2000@rocketmail.com	08057418990	2025-03-19 10:00:49.546178	16
57	Mr. and Mrs Abiwo 	abiwoabayomi@yahoo.com	08023464198	2025-03-19 10:23:56.420479	16
58	Kehinde 	talk2sweetbabyk@gmail.com	07060468768	2025-03-19 10:28:16.038307	16
59	Samuel Anyanwu	samuel3.anyanwu@gmail.com	08039352359	2025-03-19 10:58:53.25423	16
60	Salami	salami@yahoo.com	08025126294	2025-03-19 12:16:47.282645	16
61	Salami	salami24@gmail.con	08025126294	2025-03-19 12:17:55.48733	16
62	kunle Bello 	letuakb22@gmail.com	08033041075	2025-03-19 12:21:32.137918	16
63	Franko Baresi	frank_akinseye@yahoo.com	08125754922	2025-03-19 12:55:14.821471	16
64	Bhadmus Ademola 	bhadmusademola@yahoo.com	08033280306	2025-03-19 15:38:19.087648	16
65	ObaLex 	captainlex66@gmail.com	07032289890	2025-03-19 19:05:08.243616	16
66	Eniola Adeyemo	eniolaadeyemo2018@gmail.com	+2348035148598	2025-03-19 19:10:27.244156	16
67	Mr& Mrs Eyiaro olusola	olusola.eyiaro@gmaiil.com	08027612914	2025-03-19 19:10:40.596929	16
68	Olaide Oyewo	Olaideoyewo@gmail.com	08023056660	2025-03-19 19:33:53.03627	16
69	Mr & Mrs Uwatomo Adeleke	imanilucky@gmail.com	8033580532	2025-03-19 20:50:48.552159	16
70	Enobong Ekpema Uko 	enookon2002@yahoo.com	08035371854	2025-03-19 21:18:34.186069	16
71	Mrs O.T.Atunbi	otatunbi67@gmail.com	08077948532	2025-03-19 22:14:44.624979	16
74	Olumuyiwa Atitebi	muyiwatitebi@yahoo.com	9064534945	2025-03-20 07:33:25.185137	16
75	Oyolola Shuaib 	shubbyoyo1@gmail.com	08184302827	2025-03-20 08:08:27.917733	16
76	Mr & Mrs Gbenga & Omorinade Banjo	philip_banjo@yahoo.co.uk	08020957643	2025-03-20 11:13:09.547087	16
77	Mr & Mrs Loto	bensonloto@yahoo.com	08055222454	2025-03-20 12:20:56.635748	16
78	Adenike ogunniyi 	nikkyhan.aa@gmail.com	07036523737	2025-03-20 13:12:36.619224	16
79	ADELEYE OLUGBENGA 	adeleyeolugbenga01@gmail.com	08033582091	2025-03-20 13:24:06.25554	16
80	Ogunniyi Babajide Emmanuel 	bogunniyi2004@yahoo.com	08156980369	2025-03-20 13:29:50.668167	16
81	Temitope Omoyeni	Omoyeni.temitope1@gmail.com	08105056358	2025-03-20 14:27:02.932209	16
82	Damilola Archer-Birch 	damilolabirch@gmail.com	08023245941	2025-03-20 14:55:55.500713	16
83	OMOYENI OLAMILEKAN ROTIMI	omoyenirotimi1932@gmail.com	07034734520	2025-03-20 15:02:04.079236	16
84	Bolanle Sule	Bolanle.sule@gmail.com	08029575017	2025-03-20 16:20:11.522055	16
85	OLUWAFEMI VICTOR AIYEOLA 	Aiyeola2012@gmail.com	08161234872	2025-03-21 05:51:14.904501	16
86	Wilson Oletu	wilsonoletua@gmail.com	08065864900	2025-03-21 08:14:42.143828	16
87	Mr and Mrs Anifowose 	anifowoseyin@gmail.com	08023145636	2025-03-21 10:36:56.360664	16
88	Mr and mrsAdebola Ademuyiwa 	adebola@gmail.com	08033979451	2025-03-22 10:42:25.661545	16
89	Adeyemo Adewale 	adeyemoadewale9412@gmail.con	08061339412	2025-03-22 10:53:56.300932	16
90	Abisola Odunmorayo	nikodunmorayo@gmail.com	08027725837	2025-03-22 16:22:24.24864	16
91	Chinedu Duru	eduduru@gmail.com	08034918010	2025-03-22 19:50:20.394171	16
92	Okele john tochi 	ubahjude85@gmail.com	08060944200	2025-03-23 10:07:04.38412	16
93	Ubahamaka miracle 	amakabest247@gmail	09012171557	2025-03-23 10:08:12.908532	16
94	Kayode Adedayo	olukayodeadedayo@gmail.com	08035630880	2025-03-25 08:15:54.444363	16
95	Olukemi adesalu	flozzyd@gmail.com	08023247844	2025-03-25 08:35:41.498426	16
96	Adeleye 	alphaconsultingservicesng@gmail.com	07066380224	2025-03-25 11:50:50.168396	16
97	Aboyewa Okpotse 	aokpotse@gmail.com	08036277620	2025-03-26 11:11:33.367495	16
98	Adeola 	favourlove2007@yahoo.com	07025877632	2025-03-27 12:38:27.156597	16
99	Yewande Agboola	yewandenadeoye@gmail.com	08039249095	2025-03-27 20:06:55.303336	16
100	Mr and Mrs Chidi and Bunmi Udeogu	chidiudeogu@yahoo.com	08037139246	2025-03-27 21:39:31.132437	15
101	Olukayode Maiyegun	kayode_maiyegun@yahoo.com	08091112221	2025-03-30 09:18:03.235578	16
102	Fatokunboh Adedeji 	adedejifatokunboh@gmail.com	08063967470	2025-03-30 11:03:53.393206	16
103	Bankole funmilola	bankolefunmilola99@gmail.com	08028046156	2025-03-31 20:17:53.424769	16
104	Olaynka Paul	olayinkapaul1@gmail.com	08129784205	2025-03-31 20:19:27.888089	16
105	Olawunmi Ojoye	OlawunmiOjoye@gmail.com	08028046156	2025-03-31 20:24:05.68125	16
106	Angela Izomor 	angelaizomor92@gmail.com	08023090464	2025-04-02 09:20:49.300087	16
107	Uki Omokhui	ukiomokhui@yahoo.com	08023197444	2025-04-03 16:18:00.036258	16
108	BUKOLA  ADELOWO	bookiedan@gmail.com	08093333391	2025-04-04 11:49:30.398205	16
109	Aminat Ade 	rabiuaminat0@gmail.com	08077941790	2025-04-04 13:40:13.495533	16
110	Mr & Mrs Ademola idowu	Obademola@gmail.com	08035740851	2025-04-08 15:24:14.52747	16
111	Ibraheem sulaimon 	bramco2020@yahoo.com	08122262133	2025-04-10 13:52:25.039829	16
112	sobayo abdulsemiu Olaitan 	sabdulsemiu@gmail.com080	08062504074	2025-04-10 13:53:06.475172	16
113	sobayo abdulsemiu Olaitan 	sabdulsemiu@gmail.com	07014819486	2025-04-10 14:09:11.299109	16
114	ENOBONG EZEKIEL 	wonderwomaneno@gmail.com	+234 802 316 611 6	2025-04-10 19:34:33.03755	16
115	Nicky	nickyilonwafor@gmail.com	+2348033037674	2025-04-11 20:44:53.450133	15
116	Nishy	oluwanisholaolajumoke@gmail.com	08140581219	2025-04-11 21:13:17.096609	15
117	Uju Onozie	ujuglam@gmail.com	08087417485	2025-04-12 10:42:51.973427	16
118	Peace Ezeakaibeya 	peaceezeakaibeya16@gmail.com	08127720901	2025-04-12 10:44:37.613411	16
119	Daniella	daniellaharrison9@gmail.com	07012528913	2025-04-12 18:47:19.987201	16
120	Adaora Emenike	emeada04@gmail.com	08159264530	2025-04-12 19:03:39.675638	16
121	Collins Appah	appahcollins@gmail.com	08036342793	2025-04-13 10:34:36.135553	16
\.


--
-- Data for Name: guest_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.guest_type (id, name) FROM stdin;
15	Regular
16	Vips
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (id, username, password_hash, role) FROM stdin;
1	admin	scrypt:32768:8:1$I8X3Z18Xy48xjHXY$aacb3b47d465cbe49a8cf1b245250deecce666f1d1a2dc3a0e5ee790353eb682b7fa81f7b8098f0578a5903b5bacfcd1009a73a95c87a0e60f91bf16cdd85936	Admin
2	COO	scrypt:32768:8:1$1h8jYvw6kRakbNvT$247eee56cfc01f854a9184746f74da8bba135635fb7cb1431fa27cd064131775a9484ca7e3004e533d9050dbaeb6be19e7352ef8b9850fdc87e253cf8a48da61	Moderator
3	HR	scrypt:32768:8:1$shvprybkLdc5Z91S$2dde61d15ab8f46c69689be62e2fb5eccd2243b4da5f4bd4f6854a021de3836dd4e72989dc769c88f2157a889a834ef7d3580c0728703ba117cf04a80afd6163	Moderator
\.


--
-- Name: guest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.guest_id_seq', 121, true);


--
-- Name: guest_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.guest_type_id_seq', 16, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: guest guest_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest
    ADD CONSTRAINT guest_email_key UNIQUE (email);


--
-- Name: guest guest_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest
    ADD CONSTRAINT guest_pkey PRIMARY KEY (id);


--
-- Name: guest_type guest_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest_type
    ADD CONSTRAINT guest_type_name_key UNIQUE (name);


--
-- Name: guest_type guest_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest_type
    ADD CONSTRAINT guest_type_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: guest guest_guest_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guest
    ADD CONSTRAINT guest_guest_type_id_fkey FOREIGN KEY (guest_type_id) REFERENCES public.guest_type(id);


--
-- PostgreSQL database dump complete
--

