import React, { useState, useEffect } from 'react';
import { X, Calendar, Clock, User, AlertCircle } from 'lucide-react';
import { apiClient, API_ENDPOINTS } from '../../api/client';
import { Clinic, Service, Doctor, TimeSlot } from '../../types';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { format, addDays, isToday } from 'date-fns';

interface BookingModalProps {
  clinic: Clinic;
  service: Service;
  doctors: Doctor[];
  isOpen: boolean;
  onClose: () => void;
}

const BookingModal: React.FC<BookingModalProps> = ({
  clinic,
  service,
  doctors,
  isOpen,
  onClose,
}) => {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [selectedDoctor, setSelectedDoctor] = useState<string>('');
  const [availableSlots, setAvailableSlots] = useState<TimeSlot[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<TimeSlot | null>(null);
  const [patientNotes, setPatientNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [step, setStep] = useState<'date' | 'time' | 'confirm'>('date');

  // 获取可用时间段
  useEffect(() => {
    if (selectedDate && (step === 'time' || step === 'confirm')) {
      fetchAvailableSlots();
    }
  }, [selectedDate, selectedDoctor, step]);

  const fetchAvailableSlots = async () => {
    try {
      const slots = await apiClient.get<{ date: string; slots: TimeSlot[] }>(
        API_ENDPOINTS.AVAILABLE_SLOTS,
        {
          clinic_id: clinic.id,
          doctor_id: selectedDoctor || undefined,
          service_id: service.id,
          date: format(selectedDate, 'yyyy-MM-dd'),
        }
      );
      setAvailableSlots(slots.slots);
    } catch (err) {
      console.error('Failed to fetch available slots:', err);
    }
  };

  const handleDateSelect = (date: Date) => {
    setSelectedDate(date);
    setStep('time');
    setSelectedSlot(null);
  };

  const handleSlotSelect = (slot: TimeSlot) => {
    setSelectedSlot(slot);
    setStep('confirm');
  };

  const handleBookingSubmit = async () => {
    if (!selectedSlot) return;

    setIsLoading(true);
    setError(null);

    try {
      const appointmentData = {
        clinic_id: clinic.id,
        doctor_id: selectedDoctor || null,
        service_id: service.id,
        appointment_date: format(selectedDate, 'yyyy-MM-dd'),
        start_time: selectedSlot.start_time,
        notes: patientNotes,
      };

      const appointment = await apiClient.post(
        API_ENDPOINTS.APPOINTMENTS,
        appointmentData
      );

      // 预约成功，显示成功消息
      alert(`预约成功！您的预约ID是：${appointment.id}`);
      onClose();
      
      // 这里可以重定向到预约详情页面
      // navigate(`/appointments/${appointment.id}`);

    } catch (err: any) {
      setError(err.message || '预约失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* 背景遮罩 */}
        <div className="fixed inset-0 transition-opacity" aria-hidden="true">
          <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        {/* 模态框内容 */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">
                预约 {service.name}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* 进度指示器 */}
            <div className="mb-8">
              <div className="flex justify-between">
                {['date', 'time', 'confirm'].map((s, index) => (
                  <div key={s} className="flex items-center">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        step === s
                          ? 'bg-blue-600 text-white'
                          : index < ['date', 'time', 'confirm'].indexOf(step)
                          ? 'bg-green-500 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      {index + 1}
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {s === 'date' && '选择日期'}
                      {s === 'time' && '选择时间'}
                      {s === 'confirm' && '确认预约'}
                    </span>
                    {index < 2 && (
                      <div
                        className={`ml-2 w-12 h-1 ${
                          index < ['date', 'time', 'confirm'].indexOf(step)
                            ? 'bg-green-500'
                            : 'bg-gray-200'
                        }`}
                      ></div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* 步骤内容 */}
            {step === 'date' && (
              <div>
                <h4 className="text-lg font-semibold mb-4 flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  选择预约日期
                </h4>
                <DatePicker
                  selected={selectedDate}
                  onChange={handleDateSelect}
                  inline
                  minDate={new Date()}
                  maxDate={addDays(new Date(), 30)}
                  filterDate={(date) => date.getDay() !== 0} // 过滤掉周日
                  className="w-full"
                />
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-start">
                    <AlertCircle className="w-5 h-5 text-blue-500 mr-2 mt-0.5" />
                    <p className="text-sm text-blue-700">
                      请注意：周日诊所休息，节假日可能调整营业时间。
                    </p>
                  </div>
                </div>
              </div>
            )}

            {step === 'time' && (
              <div>
                <h4 className="text-lg font-semibold mb-4 flex items-center">
                  <Clock className="w-5 h-5 mr-2" />
                  选择时间段 - {format(selectedDate, 'yyyy年MM月dd日')}
                </h4>

                {/* 医生选择 */}
                {doctors.length > 0 && (
                  <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      选择医生（可选）
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      <button
                        onClick={() => setSelectedDoctor('')}
                        className={`p-3 border rounded-lg text-center ${
                          selectedDoctor === ''
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        任意医生
                      </button>
                      {doctors.map((doctor) => (
                        <button
                          key={doctor.id}
                          onClick={() => setSelectedDoctor(doctor.id)}
                          className={`p-3 border rounded-lg text-center ${
                            selectedDoctor === doctor.id
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          <div className="font-medium">{doctor.name}</div>
                          <div className="text-sm text-gray-600">
                            {doctor.title}
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* 时间段选择 */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    可用时间段
                  </label>
                  {availableSlots.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      {isToday(selectedDate) ? '今天' : format(selectedDate, 'MM月dd日')} 没有可用时间段
                    </div>
                  ) : (
                    <div className="grid grid-cols-3 gap-3">
                      {availableSlots.map((slot, index) => (
                        <button
                          key={index}
                          onClick={() => handleSlotSelect(slot)}
                          className={`p-3 border rounded-lg text-center ${
                            selectedSlot === slot
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          <div className="font-medium">
                            {slot.start_time.split(':').slice(0, 2).join(':')}
                          </div>
                          <div className="text-sm text-gray-600">
                            时长: {service.duration}分钟
                          </div>
                          {slot.doctor_id && (
                            <div className="text-xs text-blue-600">
                              指定医生
                            </div>
                          )}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex justify-between">
                  <button
                    onClick={() => setStep('date')}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                  >
                    返回选择日期
                  </button>
                  <button
                    onClick={() => selectedSlot && setStep('confirm')}
                    disabled={!selectedSlot}
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    下一步
                  </button>
                </div>
              </div>
            )}

            {step === 'confirm' && selectedSlot && (
              <div>
                <h4 className="text-lg font-semibold mb-6 flex items-center">
                  <User className="w-5 h-5 mr-2" />
                  确认预约信息
                </h4>

                {/* 预约信息摘要 */}
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">诊所</p>
                      <p className="font-medium">{clinic.name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">服务项目</p>
                      <p className="font-medium">{service.name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">预约日期</p>
                      <p className="font-medium">
                        {format(selectedDate, 'yyyy年MM月dd日')}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">预约时间</p>
                      <p className="font-medium">
                        {selectedSlot.start_time.split(':').slice(0, 2).join(':')}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">服务时长</p>
                      <p className="font-medium">{service.duration} 分钟</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">费用</p>
                      <p className="font-medium text-blue-600">
                        ${service.price.toFixed(2)}
                      </p>
                    </div>
                  </div>

                  {selectedDoctor && (
                    <div className="mt-4">
                      <p className="text-sm text-gray-600">指定医生</p>
                      <p className="font-medium">
                        {doctors.find(d => d.id === selectedDoctor)?.name}
                      </p>
                    </div>
                  )}
                </div>

                {/* 备注 */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    备注（可选）
                  </label>
                  <textarea
                    value={patientNotes}
                    onChange={(e) => setPatientNotes(e.target.value)}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="如有特殊需求，请在此备注..."
                  />
                </div>

                {error && (
                  <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-red-600 text-sm">{error}</p>
                  </div>
                )}

                <div className="flex justify-between">
                  <button
                    onClick={() => setStep('time')}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                  >
                    返回选择时间
                  </button>
                  <button
                    onClick={handleBookingSubmit}
                    disabled={isLoading}
                    className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? '处理中...' : '确认预约'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookingModal;