import os, sys, re, shutil
import json
from pathlib import Path
from datetime import *
import urllib.request
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from enums import *

def get_destination_dir(file_url, folder=None):
  store_directory = os.environ.get('STORE_DIRECTORY')
  if folder:
    store_directory = folder
  if not store_directory:
    store_directory = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(store_directory, file_url)

def get_download_url(file_url):
  return "{}{}".format(BASE_URL, file_url)

def get_all_symbols(type):
  if type == 'um':
    response = urllib.request.urlopen("https://fapi.binance.com/fapi/v1/exchangeInfo").read()
  elif type == 'cm':
    response = urllib.request.urlopen("https://dapi.binance.com/dapi/v1/exchangeInfo").read()
  else:
    response = urllib.request.urlopen("https://api.binance.com/api/v3/exchangeInfo").read()
  all_symbols = list(map(lambda symbol: symbol['symbol'], json.loads(response)['symbols']))
  all_symbols = [s for s in all_symbols if s not in get_broken_symbols()]
  return all_symbols

def get_broken_symbols():
    return ["1INCHDOWNUSDT", "1INCHUPUSDT", "AAVEBKRW", "AAVEBRL", "AAVEDOWNUSDT", "AAVEUPUSDT", "ACABUSD", "ACMBTC", "ACMBUSD", "ADAAUD", "ADABIDR", "ADABKRW", "ADADOWNUSDT", "ADAPAX", "ADAUPUSDT", "ADAUSDC", "ADXBNB", "AEBNB", "AEBTC", "AEETH", "AGIBNB", "AGIBTC", "AGIETH", "AGLDBNB", "AIONBNB", "AIONBTC", "AIONBUSD", "AIONETH", "AIONUSDT", "AKROBTC", "ALCXBUSD", "ALGOBIDR", "ALGOPAX", "ALGOTUSD", "ALGOUSDC", "ALICEBIDR", "ALICEBNB", "ALPACABNB", "ALPACABUSD", "ALPHABNB", "ALPHABUSD", "ALPINEBUSD", "AMBBNB", "AMBBUSD", "AMBETH", "AMPBNB", "AMPBTC", "ANCBNB", "ANCBTC", "ANCBUSD", "ANCUSDT", "ANKRBNB", "ANKRPAX", "ANKRTUSD", "ANKRUSDC", "ANTBUSD", "ANYBTC", "ANYBUSD", "ANYUSDT", "APEAUD", "APEBRL", "APEGBP", "API3BNB", "API3BUSD", "APPCBNB", "APPCBTC", "APPCETH", "APTBRL", "ARBNB", "ARDRBNB", "ARDRETH", "ARKBTC", "ARKETH", "ARNBTC", "ARNETH", "ASRBTC", "ASRBUSD", "ASTETH", "ASTRBUSD", "ASTRETH", "ATABNB", "ATABUSD", "ATMBTC", "ATMBUSD", "ATOMBIDR", "ATOMBRL", "ATOMPAX", "ATOMTUSD", "ATOMUSDC", "AUDBUSD", "AUDIOBUSD", "AUDUSDC", "AUDUSDT", "AUTOBTC", "AUTOBUSD", "AUTOUSDT", "AVABNB", "AVAXAUD", "AVAXBIDR", "AVAXGBP", "AXSAUD", "AXSBRL", "BALBNB", "BALBUSD", "BANDBNB", "BARBTC", "BARBUSD", "BATBNB", "BATBUSD", "BATETH", "BATPAX", "BATTUSD", "BATUSDC", "BCCBNB", "BCCBTC", "BCCETH", "BCCUSDT", "BCDBTC", "BCDETH", "BCHABCBTC", "BCHABCBUSD", "BCHABCPAX", "BCHABCTUSD", "BCHABCUSDC", "BCHABCUSDT", "BCHABUSD", "BCHDOWNUSDT", "BCHPAX", "BCHSVBTC", "BCHSVPAX", "BCHSVTUSD", "BCHSVUSDC", "BCHSVUSDT", "BCHUPUSDT", "BCHUSDC", "BCNBNB", "BCNBTC", "BCNETH", "BCPTBNB", "BCPTBTC", "BCPTETH", "BCPTPAX", "BCPTTUSD", "BCPTUSDC", "BEAMBNB", "BEAMBTC", "BEAMUSDT", "BEARBUSD", "BEARUSDT", "BELETH", "BETABNB", "BGBPUSDC", "BIFIBNB", "BIFIBUSD", "BKRWBUSD", "BKRWUSDT", "BLZBNB", "BLZBUSD", "BLZETH", "BNBAUD", "BNBBEARBUSD", "BNBBEARUSDT", "BNBBKRW", "BNBBULLBUSD", "BNBBULLUSDT", "BNBIDRT", "BNBNGN", "BNBPAX", "BNBUSDP", "BNBUSDS", "BNBUST", "BNBZAR", "BNTBUSD", "BONDBNB", "BONDETH", "BOTBTC", "BOTBUSD", "BQXBTC", "BQXETH", "BRDBNB", "BRDBTC", "BRDETH", "BSWBUSD", "BSWETH", "BTCAUD", "BTCBBTC", "BTCBKRW", "BTCIDRT", "BTCPAX", "BTCSTBTC", "BTCSTBUSD", "BTCSTUSDT", "BTCUSDP", "BTCUSDS", "BTCUST", "BTCVAI", "BTGBTC", "BTGBUSD", "BTGETH", "BTGUSDT", "BTSBNB", "BTSBTC", "BTSBUSD", "BTSETH", "BTTBNB", "BTTBRL", "BTTBTC", "BTTBUSD", "BTTCBUSD", "BTTCUSDC", "BTTEUR", "BTTPAX", "BTTTRX", "BTTTRY", "BTTTUSD", "BTTUSDC", "BTTUSDT", "BULLBUSD", "BULLUSDT", "BURGERBNB", "BURGERETH", "BUSDBKRW", "BUSDBVND", "BUSDIDRT", "BUSDNGN", "BZRXBNB", "BZRXBTC", "BZRXBUSD", "BZRXUSDT", "C98BNB", "C98BRL", "CAKEAUD", "CAKEBRL", "CAKEGBP", "CDTBTC", "CDTETH", "CELRBNB", "CELRETH", "CHATBTC", "CHATETH", "CHESSBNB", "CHZGBP", "CITYBNB", "CITYBUSD", "CKBBTC", "CKBBUSD", "CLOAKBTC", "CLOAKETH", "CLVBNB", "CMTBNB", "CMTBTC", "CMTETH", "CNDBNB", "CNDBTC", "CNDETH", "COCOSBNB", "COCOSBTC", "COCOSBUSD", "COCOSTRY", "COCOSUSDT", "COMPBNB", "COSBUSD", "COVERBUSD", "COVERETH", "CREAMBNB", "CRVBNB", "CTKBUSD", "CTXCBNB", "CVCBNB", "CVCBTC", "CVCBUSD", "CVCETH", "CVPETH", "CVXBUSD", "DAIBNB", "DAIBTC", "DAIBUSD", "DAIUSDT", "DARETH", "DASHBNB", "DASHBUSD", "DATAETH", "DCRBNB", "DCRBUSD", "DENTBTC", "DENTBUSD", "DFBUSD", "DFETH", "DGBBUSD", "DGDBTC", "DGDETH", "DIABNB", "DLTBNB", "DLTBTC", "DLTETH", "DNTBTC", "DNTBUSD", "DNTETH", "DNTUSDT", "DOCKBUSD", "DOCKETH", "DOGEAUD", "DOGEBNB", "DOGEPAX", "DOGERUB", "DOGEUSDC", "DOTAUD", "DOTBIDR", "DOTBKRW", "DOTDOWNUSDT", "DOTNGN", "DOTUPUSDT", "DREPBNB", "DUSKBNB", "DUSKPAX", "DUSKUSDC", "DYDXETH", "EASYBTC", "EASYETH", "EDOBTC", "EDOETH", "ENGBTC", "ENGETH", "ENJBNB", "ENJBRL", "ENJGBP", "EOSAUD", "EOSBEARBUSD", "EOSBEARUSDT", "EOSBULLBUSD", "EOSBULLUSDT", "EOSDOWNUSDT", "EOSPAX", "EOSTUSD", "EOSUPUSDT", "EOSUSDC", "EPSBTC", "EPSBUSD", "EPSUSDT", "EPXBUSD", "ERDBNB", "ERDBTC", "ERDBUSD", "ERDPAX", "ERDUSDC", "ERDUSDT", "ERNBNB", "ETCBRL", "ETCGBP", "ETCPAX", "ETCTUSD", "ETCUSDC", "ETHAUD", "ETHBEARBUSD", "ETHBEARUSDT", "ETHBKRW", "ETHBULLBUSD", "ETHBULLUSDT", "ETHNGN", "ETHPAX", "ETHUSDP", "ETHUST", "EVXBTC", "EVXETH", "EZBTC", "EZETH", "FARMBNB", "FARMBUSD", "FARMETH", "FIDABNB", "FILDOWNUSDT", "FILUPUSDT", "FIOBNB", "FIOBUSD", "FIROBUSD", "FIROETH", "FISBIDR", "FISBRL", "FISTRY", "FLMBNB", "FLMBUSD", "FORBNB", "FORBUSD", "FORTHBUSD", "FRONTETH", "FTMAUD", "FTMBIDR", "FTMBRL", "FTMPAX", "FTMRUB", "FTMTUSD", "FTMUSDC", "FTTBNB", "FTTBTC", "FTTETH", "FUELBTC", "FUELETH", "FUNBTC", "GALAAUD", "GALBNB", "GALBRL", "GALBUSD", "GALETH", "GALEUR", "GHSTBUSD", "GHSTETH", "GLMETH", "GLMRBNB", "GMTAUD", "GMTBRL", "GMTGBP", "GMXBUSD", "GNOBNB", "GNOBTC", "GNOBUSD", "GNTBNB", "GNTBTC", "GNTETH", "GOBNB", "GOBTC", "GRSBTC", "GRSETH", "GTCBNB", "GTOBNB", "GTOBTC", "GTOBUSD", "GTOETH", "GTOPAX", "GTOTUSD", "GTOUSDC", "GTOUSDT", "GVTBTC", "GVTETH", "GXSBNB", "GXSBTC", "GXSETH", "GXSUSDT", "HCBTC", "HCETH", "HCUSDT", "HEGICBUSD", "HEGICETH", "HIVEBNB", "HIVEBUSD", "HNTBTC", "HNTBUSD", "HNTUSDT", "HOTBNB", "HOTBRL", "HOTBTC", "HOTBUSD", "HOTEUR", "HSRBTC", "HSRETH", "ICNBTC", "ICNETH", "ICPRUB", "ICXBNB", "ICXETH", "ILVBNB", "IMXBNB", "INSBTC", "INSETH", "IOTABNB", "IQBNB", "IRISBNB", "IRISBUSD", "JASMYBNB", "JASMYBTC", "JASMYETH", "JASMYEUR", "JSTBNB", "JSTBUSD", "JUVBTC", "JUVBUSD", "KEEPBNB", "KEEPBTC", "KEEPBUSD", "KEEPUSDT", "KEYBTC", "KEYETH", "KLAYBNB", "KLAYBUSD", "KMDBUSD", "KMDETH", "KNCBNB", "KNCETH", "KP3RBNB", "KSMAUD", "KSMBNB", "KSMETH", "LENDBKRW", "LENDBTC", "LENDBUSD", "LENDETH", "LENDUSDT", "LINABNB", "LINKAUD", "LINKBKRW", "LINKDOWNUSDT", "LINKNGN", "LINKPAX", "LINKTUSD", "LINKUPUSDT", "LINKUSDC", "LITETH", "LOOMBNB", "LOOMBUSD", "LOOMETH", "LRCBNB", "LSKBNB", "LSKBUSD", "LTCDOWNUSDT", "LTCNGN", "LTCPAX", "LTCUPUSDT", "LTCUSDC", "LTOBNB", "LUNAAUD", "LUNABIDR", "LUNABNB", "LUNABRL", "LUNABTC", "LUNAETH", "LUNAEUR", "LUNAGBP", "LUNAUST", "LUNBTC", "LUNETH", "MANABIDR", "MANABNB", "MANABRL", "MATICAUD", "MATICBIDR", "MBLBNB", "MBLBTC", "MBLBUSD", "MCBNB", "MCBUSD", "MCOBNB", "MCOBTC", "MCOETH", "MCOUSDT", "MDABTC", "MDAETH", "MDTBNB", "MDTBUSD", "MDXBNB", "MFTBNB", "MFTBTC", "MFTETH", "MFTUSDT", "MINABNB", "MIRBTC", "MIRBUSD", "MIRUSDT", "MITHBNB", "MITHBTC", "MITHUSDT", "MKRBNB", "MLNBNB", "MLNBUSD", "MOBBUSD", "MODBTC", "MODETH", "MOVRBNB", "MTHBTC", "MTHETH", "MTLETH", "NANOBNB", "NANOBTC", "NANOBUSD", "NANOETH", "NANOUSDT", "NASBNB", "NASBTC", "NASETH", "NAVBNB", "NAVBTC", "NAVETH", "NBSBTC", "NBSUSDT", "NCASHBNB", "NCASHBTC", "NCASHETH", "NEBLBNB", "NEBLBTC", "NEBLBUSD", "NEBLUSDT", "NEOPAX", "NEORUB", "NEOTUSD", "NEOUSDC", "NEXOBUSD", "NKNBNB", "NKNBUSD", "NMRBUSD", "NPXSBTC", "NPXSETH", "NPXSUSDC", "NPXSUSDT", "NUAUD", "NUBNB", "NUBTC", "NUBUSD", "NULSBNB", "NULSBUSD", "NULSETH", "NURUB", "NUUSDT", "NXSBNB", "NXSBTC", "NXSETH", "OAXETH", "OGNBNB", "OGNBUSD", "OMGBNB", "OMGBTC", "OMGBUSD", "OMGETH", "ONEBIDR", "ONEETH", "ONEPAX", "ONETUSD", "ONEUSDC", "ONGBNB", "ONTBNB", "ONTETH", "ONTPAX", "ONTUSDC", "OOKIBNB", "OOKIBUSD", "OOKIETH", "ORNBUSD", "OSMOBUSD", "OSTBNB", "OSTBTC", "OSTETH", "OXTBUSD", "PAXBNB", "PAXBTC", "PAXBUSD", "PAXETH", "PAXTUSD", "PAXUSDT", "PEOPLEBNB", "PEOPLEBUSD", "PEOPLEETH", "PERLBNB", "PERLBTC", "PERLUSDC", "PHBBNB", "PHBPAX", "PHBTUSD", "PHBUSDC", "PHXBNB", "PHXBTC", "PHXETH", "PIVXBNB", "PLABNB", "PLABUSD", "PNTBTC", "POABNB", "POABTC", "POAETH", "POEBTC", "POEETH", "POLSBUSD", "POLYBNB", "POLYBTC", "POLYBUSD", "POLYUSDT", "PORTOBUSD", "POWRBNB", "POWRBUSD", "PPTBTC", "PPTETH", "PROMBNB", "PROSETH", "PSGBUSD", "PUNDIXBUSD", "QIBNB", "QKCBUSD", "QLCBNB", "QLCBTC", "QLCETH", "QNTBNB", "QSPBNB", "QSPBTC", "QSPETH", "QTUMBNB", "QTUMBUSD", "QUICKBNB", "QUICKBUSD", "RADBNB", "RADBUSD", "RAMPBTC", "RAMPBUSD", "RAMPUSDT", "RAREBNB", "RAYBUSD", "RCNBNB", "RCNBTC", "RCNETH", "RDNBNB", "RDNBTC", "RDNETH", "REEFBIDR", "REEFBTC", "REIBNB", "REIBUSD", "REIETH", "RENBNB", "RENBTCBTC", "RENBTCETH", "RENBUSD", "REPBNB", "REPBTC", "REPBUSD", "REPUSDT", "REQBUSD", "REQETH", "RGTBNB", "RGTBTC", "RGTBUSD", "RGTUSDT", "RLCBNB", "RLCBUSD", "ROSEBNB", "RPXBNB", "RPXBTC", "RPXETH", "RSRBTC", "RSRBUSD", "RUNEAUD", "RUNEGBP", "RUNETRY", "RVNBUSD", "SALTBTC", "SALTETH", "SANDAUD", "SANDBIDR", "SANDBRL", "SANTOSBRL", "SCBTC", "SCBUSD", "SCRTBUSD", "SHIBAUD", "SHIBGBP", "SHIBRUB", "SHIBUAH", "SKLBUSD", "SKYBNB", "SKYBTC", "SKYETH", "SLPBIDR", "SLPBNB", "SNGLSBTC", "SNGLSETH", "SNMBTC", "SNMBUSD", "SNMETH", "SNTBUSD", "SOLAUD", "SOLUSDC", "SPARTABNB", "SPELLBNB", "SPELLBTC", "SPELLBUSD", "SRMBIDR", "SRMBNB", "SRMBTC", "SRMBUSD", "SRMUSDT", "SSVBUSD", "STEEMBNB", "STEEMBUSD", "STMXBTC", "STMXBUSD", "STMXETH", "STORJBUSD", "STORJETH", "STORMBNB", "STORMBTC", "STORMETH", "STORMUSDT", "STPTBNB", "STPTBUSD", "STRATBNB", "STRATBTC", "STRATBUSD", "STRATETH", "STRATUSDT", "STRAXBUSD", "STRAXETH", "SUBBTC", "SUBETH", "SUNBTC", "SUNBUSD", "SUSDBTC", "SUSDETH", "SUSDUSDT", "SUSHIDOWNUSDT", "SUSHIUPUSDT", "SWRVBNB", "SWRVBUSD", "SXPAUD", "SXPBIDR", "SXPDOWNUSDT", "SXPEUR", "SXPGBP", "SXPUPUSDT", "SYSBNB", "SYSETH", "TCTBNB", "TCTBTC", "TCTUSDT", "TFUELBNB", "TFUELBUSD", "TFUELPAX", "TFUELTUSD", "TFUELUSDC", "TLMBNB", "TNBBTC", "TNBETH", "TNTBTC", "TNTETH", "TOMOBNB", "TOMOUSDC", "TORNBNB", "TORNBTC", "TORNUSDT", "TRBBNB", "TRIBEBNB", "TRIBEBTC", "TRIBEBUSD", "TRIBEUSDT", "TRIGBNB", "TRIGBTC", "TRIGETH", "TROYBNB", "TROYBTC", "TROYBUSD", "TRUBUSD", "TRURUB", "TRXAUD", "TRXDOWNUSDT", "TRXNGN", "TRXPAX", "TRXTUSD", "TRXUPUSDT", "TRXUSDC", "TUSDBNB", "TUSDBTC", "TUSDBTUSD", "TUSDETH", "TVKBUSD", "TWTBUSD", "UFTBUSD", "UMABUSD", "UNFIBNB", "UNFIETH", "UNIAUD", "UNIDOWNUSDT", "UNIEUR", "UNIUPUSDT", "USDCBNB", "USDCBUSD", "USDCPAX", "USDCTUSD", "USDPBUSD", "USDSBUSDS", "USDSBUSDT", "USDSPAX", "USDSTUSD", "USDSUSDC", "USDSUSDT", "USDTBKRW", "USDTBVND", "USTBTC", "USTBUSD", "USTUSDT", "UTKBUSD", "VENBNB", "VENBTC", "VENETH", "VENUSDT", "VETGBP", "VGXBTC", "VGXETH", "VIABNB", "VIABTC", "VIAETH", "VIBEBTC", "VIBEETH", "VIBETH", "VITEBNB", "VITEBUSD", "VOXELBNB", "VOXELETH", "VTHOBNB", "VTHOBUSD", "WABIBNB", "WABIBTC", "WABIETH", "WANBNB", "WAVESBNB", "WAVESPAX", "WAVESRUB", "WAVESTUSD", "WAVESUSDC", "WAXPBNB", "WINBTC", "WINBUSD", "WINGBNB", "WINGETH", "WINGSBTC", "WINGSETH", "WINUSDC", "WNXMBNB", "WNXMBTC", "WNXMBUSD", "WOOBUSD", "WPRBTC", "WPRETH", "WRXBNB", "WRXBTC", "WRXEUR", "WTCBNB", "WTCETH", "XEMBNB", "XEMBTC", "XEMBUSD", "XEMETH", "XLMDOWNUSDT", "XLMPAX", "XLMTUSD", "XLMUPUSDT", "XLMUSDC", "XNOBUSD", "XNOETH", "XRPAUD", "XRPBEARBUSD", "XRPBEARUSDT", "XRPBKRW", "XRPBULLBUSD", "XRPBULLUSDT", "XRPDOWNUSDT", "XRPNGN", "XRPPAX", "XRPUPUSDT", "XRPUSDC", "XTZBNB", "XTZDOWNUSDT", "XTZETH", "XTZUPUSDT", "XVGBTC", "XZCBNB", "XZCBTC", "XZCETH", "XZCUSDT", "XZCXRP", "YFIBNB", "YFIDOWNUSDT", "YFIIBNB", "YFIIBTC", "YFIIBUSD", "YFIIUSDT", "YFIUPUSDT", "YGGBNB", "YOYOBNB", "YOYOBTC", "YOYOETH", "ZECBNB", "ZECPAX", "ZECTUSD", "ZECUSDC", "ZENBNB", "ZENBUSD", "ZILBIDR", "ZILEUR", "ZRXBNB", "ZRXBUSD", "ZRXETH"]
def download_file(base_path, file_name, date_range=None, folder=None):
  download_path = "{}{}".format(base_path, file_name)
  if folder:
    base_path = os.path.join(folder, base_path)
  if date_range:
    date_range = date_range.replace(" ","_")
    base_path = os.path.join(base_path, date_range)
  save_path = get_destination_dir(os.path.join(base_path, file_name), folder)
  

  if os.path.exists(save_path):
    print("\nfile already exists! {}".format(save_path))
    return
  
  # make the directory
  if not os.path.exists(base_path):
    Path(get_destination_dir(base_path)).mkdir(parents=True, exist_ok=True)

  try:
    download_url = get_download_url(download_path)
    dl_file = urllib.request.urlopen(download_url)
    length = dl_file.getheader('content-length')
    if length:
      length = int(length)
      blocksize = max(4096,length//100)

    with open(save_path, 'wb') as out_file:
      dl_progress = 0
      print("\nFile Download: {}".format(save_path))
      while True:
        buf = dl_file.read(blocksize)   
        if not buf:
          break
        dl_progress += len(buf)
        out_file.write(buf)
        done = int(50 * dl_progress / length)
        sys.stdout.write("\r[%s%s]" % ('#' * done, '.' * (50-done)) )    
        sys.stdout.flush()

  except urllib.error.HTTPError:
    print("\nFile not found: {}".format(download_url))
    pass

def convert_to_date_object(d):
  year, month, day = [int(x) for x in d.split('-')]
  date_obj = date(year, month, day)
  return date_obj

def get_start_end_date_objects(date_range):
  start, end = date_range.split()
  start_date = convert_to_date_object(start)
  end_date = convert_to_date_object(end)
  return start_date, end_date

def match_date_regex(arg_value, pat=re.compile(r'\d{4}-\d{2}-\d{2}')):
  if not pat.match(arg_value):
    raise ArgumentTypeError
  return arg_value

def check_directory(arg_value):
  if os.path.exists(arg_value):
    while True:
      option = input('Folder already exists! Do you want to overwrite it? y/n  ')
      if option != 'y' and option != 'n':
        print('Invalid Option!')
        continue
      elif option == 'y':
        shutil.rmtree(arg_value)
        break
      else:
        break
  return arg_value

def raise_arg_error(msg):
  raise ArgumentTypeError(msg)

def get_path(trading_type, market_data_type, time_period, symbol, interval=None):
  trading_type_path = 'data/spot'
  if trading_type != 'spot':
    trading_type_path = f'data/futures/{trading_type}'
  if interval is not None:
    path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/{interval}/'
  else:
    path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/'
  return path

def get_parser(parser_type):
  parser = ArgumentParser(description=("This is a script to download historical {} data").format(parser_type), formatter_class=RawTextHelpFormatter)
  parser.add_argument(
      '-s', dest='symbols', nargs='+',
      help='Single symbol or multiple symbols separated by space')
  parser.add_argument(
      '-y', dest='years', default=YEARS, nargs='+', choices=YEARS,
      help='Single year or multiple years separated by space\n-y 2019 2021 means to download {} from 2019 and 2021'.format(parser_type))
  parser.add_argument(
      '-m', dest='months', default=MONTHS,  nargs='+', type=int, choices=MONTHS,
      help='Single month or multiple months separated by space\n-m 2 12 means to download {} from feb and dec'.format(parser_type))
  parser.add_argument(
      '-d', dest='dates', nargs='+', type=match_date_regex,
      help='Date to download in [YYYY-MM-DD] format\nsingle date or multiple dates separated by space\ndownload from 2020-01-01 if no argument is parsed')
  parser.add_argument(
      '-startDate', dest='startDate', type=match_date_regex,
      help='Starting date to download in [YYYY-MM-DD] format')
  parser.add_argument(
      '-endDate', dest='endDate', type=match_date_regex,
      help='Ending date to download in [YYYY-MM-DD] format')
  parser.add_argument(
      '-folder', dest='folder', type=check_directory,
      help='Directory to store the downloaded data')
  parser.add_argument(
      '-skip-monthly', dest='skip_monthly', default=0, type=int, choices=[0, 1],
      help='1 to skip downloading of monthly data, default 0')
  parser.add_argument(
      '-skip-daily', dest='skip_daily', default=0, type=int, choices=[0, 1],
      help='1 to skip downloading of daily data, default 0')
  parser.add_argument(
      '-c', dest='checksum', default=0, type=int, choices=[0,1],
      help='1 to download checksum file, default 0')
  parser.add_argument(
      '-t', dest='type', required=True, choices=TRADING_TYPE,
      help='Valid trading types: {}'.format(TRADING_TYPE))

  if parser_type == 'klines':
    parser.add_argument(
      '-i', dest='intervals', default=INTERVALS, nargs='+', choices=INTERVALS,
      help='single kline interval or multiple intervals separated by space\n-i 1m 1w means to download klines interval of 1minute and 1week')


  return parser


