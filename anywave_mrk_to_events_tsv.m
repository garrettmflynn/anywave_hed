function anywave_mrk_to_events_tsv(subject_name)
try
    [pp, nn, ee] = fileparts(subject_name);
    dn = strsplit(pp, filesep);
    isub = strmatch('sub-', dn);
    sub_name = dn{isub};
    ises = strmatch('ses-', dn);
    ses_name = dn{ises};
    ii = strfind(pp,sub_name);
    base_dir = pp(1:ii-1);
catch
    disp('This directory is not an EEG-BIDS structure');
    return
end

bids_eventsfname = strrep(subject_name, '_eeg.edf', '_events.tsv');

%find all users who have made annotations
if ~isempty(base_dir) && ~isequal(base_dir(end), filesep)
    base_dir = [base_dir  filesep];
end
anywave_annotations_dir = [base_dir 'derivatives' filesep 'anywave' filesep];

alld = dir([anywave_annotations_dir '*.*']);
ii = find([alld.isdir]);
alld = alld(ii);
nm = {alld.name};
ii = find(ismember(nm, '.'));
nm(ii) = [];
alld(ii) = [];
ii = find(ismember(nm, '..'));
nm(ii) = [];
alld(ii) = [];
%get subject name and subject session
marks = [];
for k=1:length(alld)
    dn = [anywave_annotations_dir alld(k).name filesep sub_name filesep ses_name filesep];
    if exist([dn 'eeg'], 'dir')
        dn = [dn 'eeg' filesep];
    end
    fx = dir([dn '*.mrk']);
    for h=1:length(fx)
        mrks = read_mrk([dn fx(h).name]);
        mrks = horzcat(mrks, repmat({alld(k).name}, size(mrks,1), 1));
        marks = vertcat(marks, mrks);
    end
end
create_tsv_event(marks, bids_eventsfname);

function mrks = read_mrk(fname)
mrks = [];
try
    fid = fopen(fname, 'r');
    st = fgetl(fid);
    fclose(fid);
catch
    return
end
if ~isequal(strtrim(st), '// AnyWave Marker File')
    return
end
[label, dummy, start, duration] = textread(fname, '%s %d %f %f', 'delimiter', char(9), 'headerlines', 1);

mrks = horzcat(label, cellfun(@num2str, num2cell(start),'UniformOutput',false), cellfun(@num2str, num2cell(duration),'UniformOutput',false));


function info = create_tsv_event(info, bids_eventsfname)
%eliminar repetidos si hubiera
umrks = {};
while ~isempty(info)
    ii = find(all(ismember(info, info(1,:)),2));
    umrks = vertcat(umrks, info(1,:));
    info(ii,:) = [];
end
info = umrks;
for k=1:size(info,1)
    for h=1:size(info,2)
        if isempty(info{k,h}), info{k,h} = 'n/a'; end
    end
end
tab = {};
for k=1:size(info,1)
    info{k,5} = '1.0';
    tab{k,1} = [info{k,2} char(9) info{k,3} char(9) info{k,1} ...
        char(9) 'All' char(9) info{k,5} char(9) info{k,4}];
end

%  eyem: Eye movements
%  chew: Chewing
%  shiv: Shivering
%  elpp: Electrode pop, Electrostatic artifacts, Lead artifacts
%  musc: Muscle artifacts
%  bckg: Background events
%  null: Undefined annotation

tab = vertcat(['onset' char(9) 'duration' char(9) 'annotation_type' char(9) 'channel' char(9) 'confidence' char(9) 'Annotator'], tab);
tab = char(tab);
dlmwrite(bids_eventsfname, tab, 'newline', 'pc', 'delimiter', '');
fjson = strrep(bids_eventsfname, '.tsv', '.json');
create_subject_json(fjson)

function create_subject_json(fjson)
json.onset.Description = 'REQUIRED. Onset (in seconds) of the event, measured from the beginning of the acquisition of the first data point stored in the corresponding task data file. Negative onsets are allowed, to account for events that occur prior to the first stored data point.';
json.duration.Description = 'REQUIRED. Duration of the event (measured from onset) in seconds';
json.annotation_type.LongName = 'Hierarchical Event Descriptors annotations';
json.annotation_type.Description = 'EEG interpretation Hierarchical Event Descriptors annotations';
json.annotation_type.Levels.eyem = 'A spike-like waveform created during patient eye movement. This artifact is usually found on all of the frontal polar electrodes with occasional echoing on the frontal electrodes';
json.annotation_type.Levels.elec = 'An electrode artifact encompasses various electrode related artifacts. Electrode pop is an artifact characterized by channels using the same electrode with an electrographic phase reversal';
json.annotation_type.Levels.musc = 'Muscle artifact. A very common, high frequency, sharp artifact that corresponds with agitation or nervousness in a patient.';
json.annotation_type.HED.eyem = 'Eye-movement-horizontal-artifact';
json.annotation_type.HED.elec = 'Electrode-pops-artifact';
json.annotation_type.HED.musc = 'EMG-artifact';
json.annotation_type.HED.eyem_musc = '(Eye-movement-horizontal-artifact , EMG-artifact)';
json.annotation_type.HED.musc_elec = '( EMG-artifact , Electrode-pops-artifact )';
json.annotation_type.HED.chew = 'Chewing-artifact';
json.annotation_type.HED.shiv = 'Movement-artifact'; %Bosch
json.annotation_type.HED.eyem_shiv = '( Eye-movement-horizontal-artifact , Movement-artifact )'; %Bosch
json.annotation_type.HED.elpp = 'Electrode-pops-artifact';
json.annotation_type.HED.eyem_elec = '( Eye-movement-horizontal-artifact , Electrode-pops-artifact )';
json.annotation_type.HED.shiv_elec = '( Movement-artifact , Electrode-pops-artifact )'; %Bosch
json.annotation_type.HED.bckg = 'Non-biological-artifact'; %Bosch
json.annotation_type.HED.null = 'Undefined annotation'; %Bosch
json.channel.LongName = 'Annotated channel';
json.channel.Description = 'List annotated channel. NA for all channels';
jsonwrite(fjson, json, 'prettyPrint', true);


function varargout = jsonwrite(varargin)
% Serialize a JSON (JavaScript Object Notation) structure
% FORMAT jsonwrite(filename,json)
% filename - JSON filename
% json     - JSON structure
%
% FORMAT S = jsonwrite(json)
% json     - JSON structure
% S        - serialized JSON structure (string)
%
% FORMAT [...] = jsonwrite(...,opts)
% opts     - structure or list of name/value pairs of optional parameters:
%              prettyPrint: indent output [Default: false]
%              replacementStyle: string to control how non-alphanumeric
%                characters are replaced {'underscore','hex','delete','nop'}
%                [Default: 'underscore']
%              convertInfAndNaN: encode NaN, Inf and -Inf as "null"
%                [Default: true]
% 
% References:
%   JSON Standard: https://www.json.org/
%   jsonencode: https://www.mathworks.com/help/matlab/ref/jsonencode.html

% Guillaume Flandin
% $Id: spm_jsonwrite.m 8031 2020-12-10 13:37:00Z guillaume $


%-Input parameters
%--------------------------------------------------------------------------
opts = struct(...
    'indent','',...
    'prettyprint',false,...
    'replacementstyle','underscore',...
    'convertinfandnan',true);
opt  = {struct([])};

if ~nargin
    error('Not enough input arguments.');
elseif nargin == 1
    filename     = '';
    json         = varargin{1};
else
    if ischar(varargin{1})
        filename = varargin{1};
        json     = varargin{2};
        opt      = varargin(3:end);
    else
        filename = '';
        json     = varargin{1};
        opt      = varargin(2:end);
    end
end
if numel(opt) == 1 && isstruct(opt{1})
    opt = opt{1};
elseif mod(numel(opt),2) == 0
    opt = cell2struct(opt(2:2:end),opt(1:2:end),2);
else
    error('Invalid syntax.');
end
fn = fieldnames(opt);
for i=1:numel(fn)
    if ~isfield(opts,lower(fn{i})), warning('Unknown option "%s".',fn{i}); end
    opts.(lower(fn{i})) = opt.(fn{i});
end
if opts.prettyprint
    opts.indent = '  ';
end
optregistry(opts);

%-JSON serialization
%--------------------------------------------------------------------------
fmt('init',sprintf(opts.indent));
S = jsonwrite_var(json,~isempty(opts.indent));

%-Output
%--------------------------------------------------------------------------
if isempty(filename)
    varargout = { S };
else
    fid = fopen(filename,'wt');
    if fid == -1
        error('Unable to open file "%s" for writing.',filename);
    end
    fprintf(fid,'%s',S);
    fclose(fid);
end


%==========================================================================
function S = jsonwrite_var(json,tab)
if nargin < 2, tab = ''; end
if isstruct(json) || isa(json,'containers.Map')
    S = jsonwrite_struct(json,tab);
elseif iscell(json)
    S = jsonwrite_cell(json,tab);
elseif ischar(json)
    if size(json,1) <= 1
        S = jsonwrite_char(json);
    else
        S = jsonwrite_cell(cellstr(json),tab);
    end
elseif isnumeric(json) || islogical(json)
    S = jsonwrite_numeric(json);
elseif isa(json,'string')
    if numel(json) == 1
        if ismissing(json)
            S = 'null';
        else
            S = jsonwrite_char(char(json));
        end
    else
        json = arrayfun(@(x)x,json,'UniformOutput',false);
        json(cellfun(@(x) ismissing(x),json)) = {'null'};
        idx = find(size(json)~=1);
        if numel(idx) == 1 % vector
            S = jsonwrite_cell(json,tab);
        else % array
            S = jsonwrite_cell(num2cell(json,setdiff(1:ndims(json),idx(1))),tab);
        end
    end
elseif isa(json,'datetime') || isa(json,'categorical')
    S = jsonwrite_var(string(json));
elseif isa(json,'table')
    S = struct;
    s = size(json);
    vn = json.Properties.VariableNames;
    for i=1:s(1)
        for j=1:s(2)
            if iscell(json{i,j})
                S(i).(vn{j}) = json{i,j}{1};
            else
                S(i).(vn{j}) = json{i,j};
            end
        end
    end
    S = jsonwrite_struct(S,tab);
else
    if numel(json) ~= 1
        json = arrayfun(@(x)x,json,'UniformOutput',false);
        S = jsonwrite_cell(json,tab);
    else
        p = properties(json);
        if isempty(p), p = fieldnames(json); end % for pre-classdef
        s = struct;
        for i=1:numel(p)
            s.(p{i}) = json.(p{i});
        end
        S = jsonwrite_struct(s,tab);
        %error('Class "%s" is not supported.',class(json));
    end
end

%==========================================================================
function S = jsonwrite_struct(json,tab)
if numel(json) == 1
    if isstruct(json), fn = fieldnames(json); else fn = keys(json); end
    S = ['{' fmt('\n',tab)];
    for i=1:numel(fn)
        key = fn{i};
        if strcmp(optregistry('replacementStyle'),'hex')
            key = regexprep(key,...
                '^x0x([0-9a-fA-F]{2})', '${native2unicode(hex2dec($1))}');
            key = regexprep(key,...
                '0x([0-9a-fA-F]{2})', '${native2unicode(hex2dec($1))}');
        end
        if isstruct(json), val = json.(fn{i}); else val = json(fn{i}); end
        S = [S fmt(tab) jsonwrite_char(key) ':' fmt(' ',tab) ...
            jsonwrite_var(val,tab+1)];
        if i ~= numel(fn), S = [S ',']; end
        S = [S fmt('\n',tab)];
    end
    S = [S fmt(tab-1) '}'];
else
    S = jsonwrite_cell(arrayfun(@(x) {x},json),tab);
end

%==========================================================================
function S = jsonwrite_cell(json,tab)
if numel(json) == 0 ...
        || (numel(json) == 1 && iscellstr(json)) ...
        || all(all(cellfun(@isnumeric,json))) ...
        || all(all(cellfun(@islogical,json)))
    tab = '';
end
S = ['[' fmt('\n',tab)];
for i=1:numel(json)
    S = [S fmt(tab) jsonwrite_var(json{i},tab+1)];
    if i ~= numel(json), S = [S ',']; end
    S = [S fmt('\n',tab)];
end
S = [S fmt(tab-1) ']'];

%==========================================================================
function S = jsonwrite_char(json)
% any-Unicode-character-except-"-or-\-or-control-character
% \" \\ \/ \b \f \n \r \t \u four-hex-digits
json = strrep(json,'\','\\');
json = strrep(json,'"','\"');
%json = strrep(json,'/','\/');
json = strrep(json,sprintf('\b'),'\b');
json = strrep(json,sprintf('\f'),'\f');
json = strrep(json,sprintf('\n'),'\n');
json = strrep(json,sprintf('\r'),'\r');
json = strrep(json,sprintf('\t'),'\t');
S = ['"' json '"'];

%==========================================================================
function S = jsonwrite_numeric(json)
if any(imag(json(:)))
    error('Complex numbers not supported.');
end
if numel(json) == 0
    S = jsonwrite_cell({});
    return;
elseif numel(json) > 1
    idx = find(size(json)~=1);
    if numel(idx) == 1 % vector
        if any(islogical(json)) || any(~isfinite(json))
            S = jsonwrite_cell(num2cell(json),'');
        else
            S = ['[' sprintf('%23.16g,',json) ']']; % eq to num2str(json,16)
            S(end-1) = ''; % remove last ","
            S(S==' ') = [];
        end
    else % array
        S = jsonwrite_cell(num2cell(json,setdiff(1:ndims(json),idx(1))),'');
    end
    return;
end
if islogical(json)
    if json, S = 'true'; else S = 'false'; end
elseif ~isfinite(json)
    if optregistry('convertinfandnan')
        S = 'null';
    else
        if isnan(json)
            S = 'NaN';
        elseif json > 0
            S = 'Infinity';
        else
            S = '-Infinity';
        end
    end
else
    S = num2str(json,16);
end

%==========================================================================
function b = fmt(varargin)
persistent tab;
if nargin == 2 && isequal(varargin{1},'init')
    tab = varargin{2};
end
b = '';
if nargin == 1
    if varargin{1} > 0, b = repmat(tab,1,varargin{1}); end
elseif nargin == 2
    if ~isempty(tab) && ~isempty(varargin{2}), b = sprintf(varargin{1}); end
end

%==========================================================================
function val = optregistry(opts)
persistent options
if isstruct(opts)
    options = opts;
else
    val = options.(lower(opts));
end

