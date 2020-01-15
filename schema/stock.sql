--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

-- Started on 2020-01-15 17:53:05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 2834 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16406)
-- Name: companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies (
    code character varying(10) NOT NULL,
    name character varying(30),
    intro text,
    manage text,
    ssrq timestamp without time zone,
    clrq timestamp without time zone,
    fxl numeric,
    fxfy numeric,
    mgfxj numeric,
    fxzsz numeric,
    srkpj numeric,
    srspj numeric,
    srhsl numeric,
    srzgj numeric,
    djzql numeric,
    wxpszql numeric,
    mjzjje numeric,
    zczb numeric,
    pos_vec numeric[]
);


ALTER TABLE public.companies OWNER TO postgres;

--
-- TOC entry 2835 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.code IS '代码';


--
-- TOC entry 2836 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.name IS '公司名';


--
-- TOC entry 2837 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.intro; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.intro IS '简介';


--
-- TOC entry 2838 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.manage; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.manage IS '经营范围';


--
-- TOC entry 2839 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.ssrq; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.ssrq IS '成立日期';


--
-- TOC entry 2840 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.fxl; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.fxl IS '发行量';


--
-- TOC entry 2841 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.fxfy; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.fxfy IS '发行费用(元）';


--
-- TOC entry 2842 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.mgfxj; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.mgfxj IS '每股发行价（元）';


--
-- TOC entry 2843 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.fxzsz; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.fxzsz IS '发行总市值(元)';


--
-- TOC entry 2844 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.srkpj; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.srkpj IS '首日开盘价(元)';


--
-- TOC entry 2845 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.srspj; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.srspj IS '首日收盘价';


--
-- TOC entry 2846 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.srhsl; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.srhsl IS '首日换手率';


--
-- TOC entry 2847 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.srzgj; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.srzgj IS '首日资金净额(元)';


--
-- TOC entry 2848 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.djzql; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.djzql IS '定价中签率';


--
-- TOC entry 2849 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.wxpszql; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.wxpszql IS '往下配售中签率';


--
-- TOC entry 2850 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.mjzjje; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.mjzjje IS '募集资金金额(元）';


--
-- TOC entry 2851 (class 0 OID 0)
-- Dependencies: 204
-- Name: COLUMN companies.zczb; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.companies.zczb IS '注册资本';


--
-- TOC entry 203 (class 1259 OID 16401)
-- Name: market; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.market (
    name "char",
    code "char" NOT NULL
);


ALTER TABLE public.market OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16428)
-- Name: quotes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotes (
    "time" timestamp without time zone NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(20),
    opening_price numeric NOT NULL,
    latest_price numeric,
    quote_change numeric,
    change numeric,
    volume numeric,
    turnover numeric,
    amplitude numeric,
    turnover_rate numeric,
    "PE_ratio" numeric,
    volume_ratio numeric,
    max_price numeric,
    min_price numeric,
    closing_price numeric NOT NULL,
    "PB_ratio" numeric,
    market character varying(20) NOT NULL
);


ALTER TABLE public.quotes OWNER TO postgres;

--
-- TOC entry 2852 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes."time"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes."time" IS '时间';


--
-- TOC entry 2853 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.code IS '代码';


--
-- TOC entry 2854 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.name IS '名称';


--
-- TOC entry 2855 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.opening_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.opening_price IS '今开';


--
-- TOC entry 2856 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.latest_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.latest_price IS '最新价';


--
-- TOC entry 2857 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.quote_change; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.quote_change IS '涨跌幅';


--
-- TOC entry 2858 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.change; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.change IS '涨跌额';


--
-- TOC entry 2859 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.volume; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.volume IS '成交量';


--
-- TOC entry 2860 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.turnover; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.turnover IS '成交额';


--
-- TOC entry 2861 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.amplitude; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.amplitude IS '振幅';


--
-- TOC entry 2862 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.turnover_rate; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.turnover_rate IS '换手率';


--
-- TOC entry 2863 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes."PE_ratio"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes."PE_ratio" IS '市盈率';


--
-- TOC entry 2864 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.volume_ratio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.volume_ratio IS '量比';


--
-- TOC entry 2865 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.max_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.max_price IS '最高价';


--
-- TOC entry 2866 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.min_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.min_price IS '最低价';


--
-- TOC entry 2867 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.closing_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.closing_price IS '昨收';


--
-- TOC entry 2868 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes."PB_ratio"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes."PB_ratio" IS '市净率';


--
-- TOC entry 2869 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN quotes.market; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.quotes.market IS '上市股市';


--
-- TOC entry 2699 (class 2606 OID 16490)
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (code);


--
-- TOC entry 2697 (class 2606 OID 16405)
-- Name: market market_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.market
    ADD CONSTRAINT market_pkey PRIMARY KEY (code);


--
-- TOC entry 2702 (class 2606 OID 16441)
-- Name: quotes quotes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_pkey PRIMARY KEY ("time", code, market);


--
-- TOC entry 2700 (class 1259 OID 16439)
-- Name: market_time_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX market_time_idx ON public.quotes USING brin (market, "time");


--
-- TOC entry 2870 (class 0 OID 0)
-- Dependencies: 2700
-- Name: INDEX market_time_idx; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON INDEX public.market_time_idx IS '股市_时间';


-- Completed on 2020-01-15 17:53:05

--
-- PostgreSQL database dump complete
--

